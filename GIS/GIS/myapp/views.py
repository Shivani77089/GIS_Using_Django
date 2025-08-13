
from django.shortcuts import render
from django.contrib import messages
from .models import HardwareData, GISNotification
from .filters import FilterTableInfo
import logging
import threading
from .DataMonitorProcedure import execute_stored_procedure_continuously
from django.http import JsonResponse

logger = logging.getLogger(__name__)

# Start the background thread for stored procedure execution
thread = threading.Thread(target=execute_stored_procedure_continuously, daemon=True)
thread.start()


def home(request):
    hardware_data = HardwareData.objects.all().order_by('-id')

    # Apply Django Filter
    filters = FilterTableInfo(request.GET, queryset=hardware_data)
    filtered_data = filters.qs

    last_displayed_id = request.session.get("last_displayed_hardware_id", 0)

    new_hardware_entries = hardware_data.filter(id__gt=last_displayed_id)

    new_hardware_names = [entry.name for entry in new_hardware_entries]

    if new_hardware_entries.exists():
        messages.success(request, f"New hardware added: {', '.join(new_hardware_names)}")
        request.session["last_displayed_hardware_id"] = new_hardware_entries.first().id

    logger.debug(f"New Hardware Data: {new_hardware_entries}")

    context = {
        'filters': filters,
        'hardware_data': filtered_data,
        'new_hardware_names': new_hardware_names
    }

    return render(request, "home.html", context)


def get_new_notifications(request):
    """Fetch latest GIS notifications where PopUp_Shown is False and update them after displaying."""
    try:
        notification_queryset = GISNotification.objects.filter(popup_shown=False).order_by('-created_date')[:1]

        latest_notifications = list(notification_queryset)

        if latest_notifications:
            notification_ids = [notification.id for notification in latest_notifications]

            notification_details = [
                f"{notification.camera_ip} at {notification.created_date.strftime('%Y-%m-%d %H:%M:%S')}"
                for notification in latest_notifications
            ]
            message_text = "New GIS notifications received: " + ", ".join(notification_details)
            messages.success(request, message_text)

            GISNotification.objects.filter(id__in=notification_ids).update(popup_shown=True)

        # JSON response
        data = [
            {
                "id": notification.id,
                "camera_ip": notification.camera_ip,
                "name": notification.name,
                "region": notification.region,
                "location": notification.location,
                "created_date": notification.created_date.strftime("%Y-%m-%d %H:%M:%S"),
                "popup_shown": notification.popup_shown
            }
            for notification in latest_notifications
        ]

        return JsonResponse({
            "notifications": data,
            "message": message_text if latest_notifications else "No new notifications.",
        })

    except Exception as e:
        logger.exception("Error fetching notifications")
        return JsonResponse({"error": "Failed to fetch notifications"}, status=500)



#
# import logging
# from django.shortcuts import render
# from .models import HardwareData
# import logging
# from .filters import FilterTableInfo
# from django.contrib import messages
#
# logger = logging.getLogger(__name__)
#
#
# def home(request):
#     hardware_data = HardwareData.objects.all().order_by('-id')
#
#     # Apply Django Filter
#     filters = FilterTableInfo(request.GET, queryset=hardware_data)
#     filtered_data = filters.qs
#
#     # Get the latest hardware entry
#     latest_hardware = hardware_data.first()
#
#     if latest_hardware:
#         messages.success(request, f"New hardware added: {latest_hardware.name}")
#
#     logger.debug(f"Latest Hardware Data: {latest_hardware}")
#
#     context = {
#         'filters': filters,
#         'hardware_data': filtered_data
#     }
#
#     return render(request, "home.html", context)
#
