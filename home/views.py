from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

import json
import requests
from .forms import *
# Create your views here.

URL_ENDPOINT = 'http://103.141.140.189:8091/api/v1/path'
DIR_TO_AUDIO = 'media/audios/' 

class Home(View):

    def get(self, request):
        recorderForm = RecorderForm()
        no_recorder = min(len(RecorderModel.objects.all()),10)
        recorders = list(RecorderModel.objects.all())[-no_recorder:]
        
        recorder0 = RecorderModel.objects.get(id=27)
        recorder1 = RecorderModel.objects.get(id=26)
        recorder2 = RecorderModel.objects.get(id=28)
        recorder3 = RecorderModel.objects.get(id=22)

        params = {'form' : recorderForm, 'recorders': recorders, 'recorder0': recorder0,
        'recorder1': recorder1,'recorder2': recorder2,'recorder3': recorder3}
        return render(request, template_name='home/index.html',context=params)

    def post(self, request):
                   
        recorderForm = RecorderForm(request.POST)
        if recorderForm.is_valid():
            text = recorderForm.cleaned_data['content']
            voiceId = recorderForm.cleaned_data['gender']
            audio = {'text':text, 'voiceId':str(voiceId)}
            api_response = requests.post(URL_ENDPOINT, audio)
            json_response = json.loads(api_response.text)
            try:
                url_audio = json_response['data']['url']
            except:
                return redirect('.')
            filename = url_audio.split('/')[-1] 
            # save audio 
            r = requests.get(url_audio, allow_redirects=True)
            open(DIR_TO_AUDIO + filename , 'wb').write(r.content)
            # save record
            record = RecorderModel(content=text, gender=voiceId, audio= r'audios/'+filename)
            record.save()

        return redirect('.')
        
    