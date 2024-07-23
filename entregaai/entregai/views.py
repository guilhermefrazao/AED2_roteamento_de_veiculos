from django.shortcuts import render
from django.http import JsonResponse
from .forms import AlgorithmParametersForm
from .route_generator import generate_and_save_maps

def index(request):
    if request.method == 'POST':
        form = AlgorithmParametersForm(request.POST)
        if form.is_valid():
            params = form.save()
            try:
                map_filenames = generate_and_save_maps(
                    location_point=(params.latitude, params.longitude),
                    num_vehicles=params.number_of_vehicles,
                    base_path='entregai/static/maps'
                )
                map_urls = [f'{filename}' for filename in map_filenames]
                return JsonResponse({'success': True, 'map_urls': map_urls})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
    else:
        form = AlgorithmParametersForm()
    return render(request, 'entregai/index.html', {'form': form})
