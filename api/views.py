from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Device, DeviceReading
import json


def home_view(request):
    last_reading = []
    devices = Device.objects.all()


    for device in devices:
        latest_reading = DeviceReading.objects.filter(device = device).order_by('-created_at').first()

        if latest_reading:
            last_reading.append(latest_reading)


    total_devices = Device.objects.count()
    total_readings = DeviceReading.objects.count()

    context = {
            'latest_readings': last_reading,
            'total_devices': total_devices,
            'total_readings': total_readings,
            'latest_reading' : last_reading[0] if last_reading else None
        }

    #JS AJAX request ise json döndürmek için#
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Data updated'
        })

    return render(request, 'home.html', context)



def device_detail_view(request, device_id):
    device = get_object_or_404(Device, device_id = device_id)
    veri_gecmisi = DeviceReading.objects.filter(device = device).order_by('-created_at')[:100]

    edit_reading_id = request.GET.get('edit')
    edit_reading = None

    if edit_reading_id:
        try:
            edit_reading = DeviceReading.objects.get(id=edit_reading_id, device=device)
        except DeviceReading.DoesNotExist:
            pass

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'edit_reading' and edit_reading:
            new_properties = {}
            invalid = False

            for key , value in request.POST.items():
                if key.startswith('property_'):
                    prop_key = key.replace('property_', '')
                    new_properties[prop_key] = value

            for key , value in new_properties.items():
                try:
                    if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                        new_properties[key] = int(value)
                    else:
                        new_properties[key] = float(value)

                except (ValueError,TypeError):
                    messages.error(request, 'Geçersiz bir değer girdiniz!')
                    invalid = True

            if invalid:
                return redirect(f'/device/{device_id}/?edit={edit_reading_id}')

            edit_reading.properties = new_properties
            edit_reading.save()

            return redirect('device_detail', device_id = device.device_id)


        elif action == 'delete_reading' and edit_reading:
            edit_reading.delete()
            return redirect('device_detail', device_id = device.device_id)


    context = {
               'device': device,
               'veri_gecmisi' : list(veri_gecmisi),
               'edit_reading' : edit_reading,
               }

    return render(request, 'cihaz_detay.html', context)





def compare_devices_view(request):
    devices = Device.objects.all()
    device_1 = request.GET.get('device_1_id')
    device_2 = request.GET.get('device_2_id')

    context = {
        'devices' : devices ,
        'selected_device1' : device_1 ,
        'selected_device2' : device_2
    }
    if device_1 and device_2:
        try:
            device1 = Device.objects.get(device_id = device_1)
            device2 = Device.objects.get(device_id = device_2)

            reading1 = DeviceReading.objects.filter(device = device1).order_by('-created_at').first()
            reading2 = DeviceReading.objects.filter(device = device2).order_by('-created_at').first()
            context.update({
                'device1' : device1,
                'device2' : device2,
                'reading1' : reading1,
                'reading2' : reading2
            })
            if reading1 and reading1.properties and reading2 and reading2.properties:
                common_properties = set(reading1.properties.keys()) & set(reading2.properties.keys())
                if common_properties:
                    comparing_data = []

                    for prop in common_properties:
                        value1 = reading1.properties[prop]
                        value2 = reading2.properties[prop]
                        try:
                            val1_num = float(value1)
                            val2_num = float(value2)
                            difference = abs(val1_num - val2_num)

                        except (ValueError,TypeError):
                            difference = None

                        comparing_data.append({
                            'property' : prop,
                            'value1' : value1,
                            'value2' : value2,
                            'difference' : difference
                        })
                    context['comparing_data'] = comparing_data
                    context['has_common_properties'] = True
                else:
                    context['has_common_properties'] = False
                    context['no_commons_message'] = "Cihazlar Ortak Özelliklere Sahip Değil!"

            else:
                context['has_common_properties'] = False
                context['has_no_property'] = "Veri Bulunamadı!!"

        except Device.DoesNotExist:
            context['error'] = "Cihaz Bulunamadı!!"

    return render(request, 'compare_devices.html', context)





#API DEFINITIONS

@csrf_exempt
def add_device(request):
    if request.method == "POST":
        data = json.loads(request.body)
        device_id = data.get('device_id')

        if Device.objects.filter(device_id = device_id).exists():
            return JsonResponse({'error':'Device already exists'}, status=400)

        else:
            Device.objects.create(
                name = data.get('name'),
                device_id = data.get('device_id'),
            )
            return JsonResponse({'status':'Successfully added'},status=200)



@csrf_exempt
def add_data(request,device_id):
    if request.method == "POST":
        data = json.loads(request.body)


        try:
            device = Device.objects.get(device_id = device_id)

        except Device.DoesNotExist:
            return JsonResponse({'error':'Device not found'}, status=404)


        new_data = {}
        for key, value in data.items():
                new_data[key] = value

        DeviceReading.objects.create(
            device = device,
            properties = new_data,
        )
        return JsonResponse({'status':'Successfully added'},status=200)

    else:
        return JsonResponse({'error':'Device does not exist'}, status=400)





@csrf_exempt
def update_data(request,device_id):
    if request.method == 'PATCH':
        data = json.loads(request.body)
        device = Device.objects.get(device_id = device_id)
        latest_reading = DeviceReading.objects.filter(device = device).order_by('-created_at').first()

        if latest_reading:
            new_properties = latest_reading.properties.copy()

        else:
            new_properties = {}

        for key, value in data.items():
            if key != 'device_id':
                new_properties[key] = value

        DeviceReading.objects.create(
            device = device,
            properties = new_properties,
        )
        return JsonResponse({'status': 'Succesfully updated'},status=200)



@csrf_exempt
def delete_data(request,device_id):
    if request.method == 'DELETE':
        if device_id:
            device = Device.objects.get(device_id = device_id)
            DeviceReading.objects.filter(device = device).delete()
            return JsonResponse({'status': 'Succesfully deleted'},status=200)

        else:
            return JsonResponse({'error':'Device not found'}, status=404)




@csrf_exempt
def delete_device(request,device_id):
    if request.method == 'DELETE':

        if device_id:
            device =Device.objects.get(device_id = device_id)
            device.delete()
            return JsonResponse({'status': 'Succesfully deleted'},status=200)

        else:
            return JsonResponse({'error':'Device not found'}, status=404)
