from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from FirstProject.views import hello, current_time, shifted_time, template_time
from books import views as books
from mts import views as mts

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'FirstProject.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^hello/$', hello),
                       url(r'^time/$', current_time),
                       url(r'^shift_time/(\d{1,2})/(\d{1,2})/$', shifted_time),
                       url(r'^template_time/$', template_time),
                       url(r'^search_book/$', books.search_form),
                       url(r'^search_results/$', books.search_results),
                       url(r'^load_file/', mts.load_file),
                       url(r'^analyze/', mts.calls_analyze),
                      )

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
