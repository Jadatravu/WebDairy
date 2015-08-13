from django.conf.urls import patterns, url

from django.conf.urls import url, include
from rest_framework import routers
from modelsapp import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'usersearch', views.UserSearchSet, base_name="users")

urlpatterns = patterns('modelsapp.views',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^Contacts/api/subjects/$','getsubjectlist',name='getsubjectlist'),
    url(r'^Contacts/api/namesearchlist/$','namesearchlist',name='namesearchlist'),
    url(r'^Contacts/class/addsubject/$','addsubject',name='addsubject'),
    url(r'^Contacts/class/editsubject/$','editsubject',name='editsubject'),
    url(r'^Contacts/class/searchsubject/$','searchsubject',name='searchsubject'),
    url(r'^Contacts/class/subjecttodep/$','subjecttodep',name='subjecttodep'),
    url(r'^Contacts/class/addtest/$','addtest',name='addtest'),
    url(r'^Contacts/class/viewtest/$','viewtest',name='viewtest'),
    url(r'^Contacts/class/edittest/$','edittest',name='edittest'),
    url(r'^Contacts/class/reportcard/$','reportcard',name='reportcard'),
    url(r'^Contacts/admin/approveleave_form/$','approveleave_form',name='approveleave_form'),
    url(r'^Contacts/admin/addacademicyear/$','addacademicyear',name='addacademicyear'),
    url(r'^Contacts/admin/approveleaveform/(\d+)/$','approveleaveform',name='approveleaveform'),
    url(r'^Contacts/admin/approveleave/$', 'approveleave', name='approveleave'),
    url(r'^Contacts/applyleave/$', 'applyleaveform', name='applyleaveform'),
    url(r'^Contacts/admin/releaseleaves/$', 'releaseleaves', name='releaseleaves'),
    url(r'^Contacts/admin/skilltitleaddform/$', 'skilltitleaddform', name='skilltitleaddform'),
    url(r'^Contacts/admin/addholidayform/$', 'addholidayform', name='addholidayform'),
    url(r'^Contacts/admin/skillsearchform/$', 'skillsearchform', name='skillsearchform'),
    url(r'^Contacts/skillcontactaddform/$', 'skillcontactaddform', name='skillcontactaddform'),
    url(r'^Contacts/admin/contactform/$', 'contactform', name='contactform'),
    url(r'^Contacts/admin/jobtitleform/$', 'jobtitleform', name='jobtitleform'),
    url(r'^Contacts/admin/departmentform/$', 'departmentform', name='departmentform'),
    url(r'^Contacts/admin/supervisorform/$', 'supervisorform', name='supervisorform'),
    url(r'^Contacts/admin/esearchform/$', 'esearchform', name='esearchform'),
    url(r'^Contacts/admin/editsearchform/$', 'editsearchform', name='editsearchform'),
    url(r'^Contacts/admin/deletesearchform/$', 'deletesearchform', name='deletesearchform'),
    url(r'^Contacts/adminindex/$', 'adminindex', name='adminindex'),
    url(r'^Contacts/login/', 'login',name='login'),
    url(r'^Contacts/logout/','logout',name='logout'),
    url(r'^Contacts/viewcontact/(\d+)/$','viewcontact',name='viewcontact'),
    url(r'^Contacts/viewdepcontact/(\d+)/$','viewdepcontact',name='viewdepcontact'),
    url(r'^Contacts/viewdepsubject/(\d+)/$','viewdepsubject',name='viewdepsubject'),
    url(r'^Contacts/viewdeptest/(\d+)/$','viewdeptest',name='viewdeptest'),
    url(r'^Contacts/editcontact/(\d+)/$','editcontactform',name='editcontactform'),
    url(r'^Contacts/deletecontact/(\d+)/$','deletecontactform',name='deletecontactform'),
    #url(r'^Contacts/logout/', 'django.contrib.auth.logout'),
)
