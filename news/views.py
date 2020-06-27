import itertools

from django.db.models.functions import datetime
from django.shortcuts import render
from django.http import HttpResponse
from hypernews.settings import JSON_DATA
from copy import deepcopy
from django.http import HttpResponseRedirect


# Create your views here.
def index(request):
    return HttpResponseRedirect('/news/')


def news_one(request, news_id: int):
    data = {'news': JSON_DATA[news_id - 1]}
    context = {'info': data}
    return render(request, 'some_news.html', context)


def simple_date_fun(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")


def sorted_news(request):
    render_data = deepcopy(JSON_DATA)
    render_data.sort(key=lambda x: datetime.datetime.strptime(x['created'], '%Y-%m-%d %H:%M:%S'), reverse=True)

    q = request.GET.get('q')
    if q is not None:
        render_data = [news for news in render_data if q in news['title']]

    all_news = [{'date': date, 'values': list(news)} for date, news in
                itertools.groupby(render_data, lambda x: simple_date_fun(x['created']))]

    return render(request, 'news.html', {'info': all_news})


# JSON_DATA.sort(key=lambda x: datetime.datetime.strptime(x['created'], '%Y-%m-%d %H:%M:%S')) СОРТИРОВКА ЛИСТА ПО ДАТЕ

def create_news(request):
    if request.method == "POST":
        text = request.POST.get('text')
        title = request.POST.get('title')
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        link = len(JSON_DATA) + 1

        JSON_DATA.append({'created': str(date), 'text': text, 'title': title, "link": link})

        return HttpResponseRedirect('/news/')

    return render(request, 'ex.html')
