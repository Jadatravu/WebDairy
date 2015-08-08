from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf

from modelsapp.models import Contact
from modelsapp.forms import ContactForm
from modelsapp.models import JobTitle
from modelsapp.forms import JobTitleForm

from modelsapp.models import Department
from modelsapp.forms import DepartmentForm

from modelsapp.models import Supervisor
from modelsapp.forms import SupervisorForm
from modelsapp.forms import ViewContactForm

from modelsapp.models import Address
from modelsapp.forms import ESearchForm

from modelsapp.models import SkillTitle
from modelsapp.forms import SkillTitleForm

from modelsapp.models import Skill

from modelsapp.models import Holiday

from modelsapp.models import LeaveBalance

from modelsapp.models import Leave

from modelsapp.models import Subject
from modelsapp.forms import SubjectForm

from modelsapp.models import AcademicYear
from modelsapp.forms import AddAcademicYearForm

from modelsapp.models import Test
import datetime
import django

from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login,
    logout as auth_logout, get_user_model, update_session_auth_hash)
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse

from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm

from django.contrib.auth import authenticate, logout
from django.contrib import auth

from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

import json
from django.http import HttpResponse

#rest imports start
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from modelsapp.serializers import RestAppSerializer
from rest_framework import permissions
#rest imports end



import logging
logger = logging.getLogger(__name__)


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = RestAppSerializer

class UserSearchSet(viewsets.ModelViewSet):
    def get_queryset(self):
        cons = Contact.objects.filter(first_name__contains = self.request.GET['key'])
        return cons
    serializer_class = RestAppSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (permissions.IsAuthenticated,)

def namesearchlist(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("log 0 =>request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    results=[]
    if request.method == 'POST':
        logger.debug("this is post method ")
    if request.method == 'GET':
        logger.debug("this is GET method ")
        logger.debug("len %d"% len(request.GET.keys()))
        for key in request.GET.keys():
            logger.debug(key)
        logger.debug(str(request.GET["term"]))
        a_list = AcademicYear.objects.filter(current = True)
        con_list = a_list[0].contact_set.filter(first_name__contains=str(request.GET["term"]))
        for con in con_list:
           con_dict={}
           con_dict_str = str(con.first_name).replace(" ","_")
           results.append(con_dict_str)
        con_list = a_list[0].contact_set.filter(sur_name__contains=str(request.GET["term"]))
        for con in con_list:
           con_dict={}
           con_dict_str = str(con.sur_name).replace(" ","_")
           results.append(con_dict_str)       
        con_list = a_list[0].contact_set.filter(last_name__contains=str(request.GET["term"]))
        for con in con_list:
           con_dict={}
           con_dict_str = str(con.last_name).replace(" ","_")
           results.append(con_dict_str) 
        """
        for nl1 in results:
           logger.debug(str(nl1))
        """
        results_set = set( results )   
        """
        for nl in list(results_set):
           logger.debug(str(nl))  
        """
    data = json.dumps(list(results_set))
    #data = json.dumps([sub.sub_name for sub in sub_list])
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def getsubjectlist(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("log 0 =>request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    results=[]
    if request.method == 'POST':
        logger.debug("this is post method ")
    if request.method == 'GET':
        logger.debug("this is GET method ")
        logger.debug("len %d"% len(request.GET.keys()))
        for key in request.GET.keys():
            logger.debug(key)
        a_list = AcademicYear.objects.filter(current = True)
        sub_list = a_list[0].subject_set.filter(sub_name__contains=request.GET["term"])
        for sub in sub_list:
           sub_dict={}
           sub_dict_str = str(sub.sub_name).replace(" ","_")
           results.append(sub_dict_str)
    data = json.dumps(results)
    #data = json.dumps([sub.sub_name for sub in sub_list])
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def approveleave(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("log 0 =>request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    con_list = Contact.objects.filter(login_name=request.user.username)
    logger.debug ("con_list len  %d"%len(con_list))
    lea_list=[]
    if (len(con_list) > 0):
        lea_list = Leave.objects.filter(app_id=con_list[0].id)

    logger.debug ("lea_list len  %d"%len(lea_list))
    return render_to_response(
                      'approveleave.html',
                       {'user':request.user,'leave_list':lea_list},
                       context_instance=RequestContext(request)
                     )#
    pass

def approveleave_form(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("log 0 =>request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    if request.method == 'POST':
        comment = request.POST['comment']
        leave_id = request.POST['leave_id']
        lea = Leave.objects.get(id=leave_id)
        lea.app_date=datetime.datetime.now()
        lea.app_comment=comment
        lea.state=1 #approved
        lea.save()
        logger.debug("leave state : %d"%lea.state)
        logger.debug("leave app comment : %s"%lea.app_comment)
        return render_to_response(
                      'approveleaveform.html',
                       {'user':request.user,'leave':lea},
                       context_instance=RequestContext(request)
                     )#

def approveleaveform(request,leave_id):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("log 0 =>request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    lea = Leave.objects.get(id=leave_id)
    return render_to_response(
                      'approveleaveform.html',
                       {'user':request.user,'leave':lea},
                       context_instance=RequestContext(request)
                     )#


def applyleaveform(request):
    #if (request.user.is_authenticated() == False):
    #if request.user.is_authenticated() and request.user.is_superuser:
    if request.user.is_authenticated():
        logger.debug ("log 0 =>request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    logger.debug("this is  apply leaves form")
    message=""
    if request.method == 'POST':
        fm_date = request.POST['datevalue']
        t_date = request.POST['datevalue1']
        comment = request.POST['comment']
        con_id = request.POST['contact_id']
        tpe = request.POST['type']
        logger.debug("from date => %s"%fm_date)
        logger.debug("to date => %s"%t_date)
        logger.debug("comment => %s"%comment)
        from_date_list = str(fm_date).split('/')
        to_date_list = str(t_date).split('/')
        if (len(from_date_list) > 1 and len(to_date_list) > 1):
             f_date = datetime.date(int(from_date_list[2]),int(from_date_list[0]),int(from_date_list[1]))
             t_date = datetime.date(int(to_date_list[2]),int(to_date_list[0]),int(to_date_list[1]))
             d=f_date
             no_applying_leaves = 1 
             # no applying leaves will initialized to 1, as the dates are inclusive in calculating the no of leaves
             #calculate no_of_days_leave considering holidays,earlier applied leaves
             time_delta = datetime.timedelta(1)
             while ((t_date -d) > datetime.timedelta(0)):
                 is_h_day = 0
                 h_day_list=Holiday.objects.all()
                 #check d is holiday
                 for hd in h_day_list:
                     if hd.h_date == d:
                        is_h_day=1
                 #check d is a saturday/sunday
                 if is_h_day == 0:
                     if (d.weekday() == 5 or d.weekday() ==6) :
                        is_h_day=1
                 #check d is already applied leave day 
                 if is_h_day == 0:
                    contact=Contact.objects.get(id=con_id)
                    leave_list = Leave.objects.filter(requester=contact)
                    for leave in leave_list:
                        if leave.count == 1:
                           if leave.from_date == d:
                               is_h_day=1
                        elif leave.count > 1:
                            l_day = leave.from_date
                            while (l_day < leave.to_date):
                                if l_day == d:
                                    is_h_day=1
                                l_day = l_day + time_delta
                 if is_h_day == 0:
                     no_applying_leaves += 1
                 d=d+time_delta
             #if the leave balance is sufficient update leave_balance_table,Leave Table
             logger.debug("no_applying leaves => %d"%no_applying_leaves)
             cont=Contact.objects.get(id=con_id)
             le_balance=LeaveBalance.objects.filter(contact=cont)
             logger.debug(le_balance[0].sick_leave_balance)
             logger.debug(le_balance[0].earned_leave_balance)
             logger.debug("type => %d"%int(tpe))
             if (int(tpe) == 0): # sick leave
                if ((no_applying_leaves > 0) and ( le_balance[0].sick_leave_balance - no_applying_leaves > -1)):
                     logger.debug("sick no_applying leaves => %d"%no_applying_leaves)
                     logger.debug("app_id => %d"%cont.supervisor.sup_id)
                     logger.debug("app_id => %d"%cont.supervisor_id)
                     apply_leave = Leave(requester=cont, app_id=cont.supervisor.sup_id,from_date=f_date,to_date=t_date,count=no_applying_leaves,state=0,type=tpe,req_comment=comment,app_comment="-")
                     apply_leave.save()
                     #le_balance[0].sick_leave_balance = le_balance[0].sick_leave_balance - no_applying_leaves
                     sick_leave_bal = le_balance[0].sick_leave_balance 
                     sick_leave_bal = sick_leave_bal - no_applying_leaves
                     le_balance[0].sick_leave_balance = sick_leave_bal
                     logger.debug("sick_leave_ balance %d"%le_balance[0].sick_leave_balance)
                     logger.debug("sick_leave_ bal %d"%sick_leave_bal)
                     leave_id = le_balance[0].id
                     le_bal=LeaveBalance.objects.get(id=leave_id)
                     le_bal.sick_leave_balance = sick_leave_bal
                     le_bal.save()
                     logger.debug("sick_leave_ balance %d"%le_balance[0].sick_leave_balance)
                     logger.debug("sick_leave_ balance %d"%le_bal.sick_leave_balance)
                else:
                    #if (( le_balance[0].sick_leave_balance - no_applying_leaves < 0)):
                    message = "Insufficient Leave Balance"
             elif (int(tpe) == 1): # earned Leave
                if ((no_applying_leaves > 0) and ( le_balance[0].earned_leave_balance - no_applying_leaves > -1)):
                     logger.debug("earned no_applying leaves => %d"%no_applying_leaves)
                     apply_leave = Leave(requester=cont, app_id=cont.supervisor_id,from_date=f_date,to_date=t_date,count=no_applying_leaves,state=0,type=tpe,req_comment=comment,app_comment="-")
                     apply_leave.save()
                     earned_leave_bal = le_balance[0].earned_leave_balance 
                     earned_leave_bal = earned_leave_bal -  no_applying_leaves
                     leave_id = le_balance[0].id
                     le_bal=LeaveBalance.objects.get(id=leave_id)
                     le_bal.earned_leave_balance = earned_leave_bal
                     le_bal.save()
                     logger.debug("earned_leave balance %d"%le_bal.earned_leave_balance)
                else:
                    #if (( le_balance[0].earned_leave_balance - no_applying_leaves < 0)):
                    message = "Insufficient Leave Balance"
                 
             #send error message if the leave balance is not sufficient
    leave_balance_list=[]
    contacts_list = Contact.objects.filter(login_name=request.user.username) 
    for con in contacts_list:
       logger.debug("id => %d"%con.id)
       le_bl=LeaveBalance.objects.filter(contact=con)
       leave_balance_list.append(le_bl[0])
    logger.debug("leave_balance_list => %d"%len(leave_balance_list))
    logger.debug("user => %s"%request.user.username)
    logger.debug("len => %d"%len(contacts_list))
    return render_to_response(
                      'applyleave.html',
                       {'user':request.user,'contacts_list':contacts_list, 'msg':message,'leave_bal_list':leave_balance_list},
                       context_instance=RequestContext(request)
                     )#

def releaseleaves(request):
    sick_leave_add = 1
    earned_leave_add = 1
    #if (request.user.is_authenticated() == False):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("log 0 =>request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    logger.debug("this is  release leaves form")
    contacts_list = Contact.objects.all()
    for con in contacts_list:
       le_balance=LeaveBalance.objects.filter(contact=con)
       if (len(le_balance) > 0):
            le_balance[0].sick_leave_balance += sick_leave_add
            le_balance[0].earned_leave_balance +=earned_leave_add 
            le_balance[0].save()
       else:
          le_bal = LeaveBalance(contact=con, sick_leave_balance=sick_leave_add, earned_leave_balance=earned_leave_add)
          le_bal.save()
    le_bal_list=LeaveBalance.objects.all()
    logger.debug ("h_len %d "%len(le_bal_list))
    return render_to_response(
                      'releaseleaves.html',
                       {'leave_balance_list': le_bal_list, 'user':request.user},
                       context_instance=RequestContext(request)
                     )#

def addholidayform(request):
    #if (request.user.is_authenticated() == False):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("log 0 =>request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    logger.debug("this is  add holiday form")
    if request.method == 'POST':
        da_value = request.POST['datevalue']
        h_name = request.POST['h_name']
        logger.debug ("h_date %s "%da_value)
        da_value_list = da_value.split('/')
        holiday_date=da_value_list[2]+str('-')+da_value_list[0]+str('-')+da_value_list[1]
        h_day=Holiday(holiday_name=h_name,h_date=holiday_date)
        h_day.save()
        return HttpResponseRedirect(reverse('modelsapp.views.addholidayform'))
    holidays_list=Holiday.objects.filter(h_date__year=datetime.datetime.now().year)
    #holidays_list=[]
    logger.debug ("h_len %d "%len(holidays_list))
    return render_to_response(
                      'addholiday.html',
                       {'holidays': holidays_list, 'user':request.user},
                       context_instance=RequestContext(request)
                     )#

def skillcontactaddform(request):
    #if (request.user.is_authenticated() == False):
    #if request.user.is_authenticated() and request.user.is_superuser:
    if request.user.is_authenticated():
        logger.debug ("log 0 =>request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    logger.debug("this is skill title contact add form")
    message = str("")
    if request.method == 'POST':
        exper_years1 = request.POST['years']
        skill_title1 = request.POST['title']
        exper_level1 = request.POST['exper']
        con_id = request.POST['con_id']
        contact=Contact.objects.get(id=con_id)
        skill_list = contact.skill_set.filter(skill_name = skill_title1)
        if ( len(skill_list) == 0):
           sk=Skill(skill_name=skill_title1,exp_years=exper_years1,exp_level=exper_level1)
           sk.save()
           sk.contact.add(contact)
        else:
           message = str("Skill Already in the Contact Skills List")
        #return HttpResponseRedirect(reverse('modelsapp.views.skillcontactaddform'))
    else:
        pass
    logger.debug (" log 1 =>request user %s is authenticated"%request.user.username)
    contacts_list=Contact.objects.filter(login_name__contains=request.user.username)
    logger.debug (" log 1 =>contacts_list len %d is authenticated"%len(contacts_list))
    skill_contact_list={}
    for ct in contacts_list:
        skill_contact_list[ct]=ct.skill_set.all()
           
    if( len(contacts_list) > 0):
             skill_list=contacts_list[0].skill_set.all()
             logger.debug (" log 1 =>skill_list len %d is authenticated"%len(skill_list))
             tit_list = SkillTitle.objects.all() 
             year_list=[1,2,3,4,5,6,7,8,9,10,11,12]
             exp_level_list=[1,2,3,4,5]
             return render_to_response(
                      'skilladdcontact.html',
                       {'msg':message, 'skill': skill_list,'ylist': year_list,'elist':exp_level_list,'title_list':tit_list,'user':request.user, 'contact_list':contacts_list,'skill_contact_list':skill_contact_list},
                       #{'form': form},
                       context_instance=RequestContext(request)
                     )#

def skilltitleaddform(request):
    #if (request.user.is_authenticated() == False):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    logger.debug("this is skill title add form")
    if request.method == 'POST':
        form = SkillTitleForm(request.POST)
        if form.is_valid():
            newdoc = SkillTitle(skill_title = request.POST['skill_title'])
            newdoc.save()
            return HttpResponseRedirect(reverse('modelsapp.views.skilltitleaddform'))
    else:
        form = SkillTitleForm()
    documents = SkillTitle.objects.all()
    return render_to_response(
        'skilltitleadd.html',
        {'skilltitle': documents, 'form': form,'user':request.user},
        #{'form': form},
        context_instance=RequestContext(request)
    )#
       

def deletecontactform(request,con_id):
    #if (request.user.is_authenticated() == False):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    logger.debug("this is edit contact form")
    contacts = Contact.objects.all()
    con_l = [] 
    for con in contacts:
        if int(con.supervisor.sup_id) == int(con_id):
           logger.debug( con.first_name)
           con_l.append(con)
    logger.debug("contacts len %s"%str(len(con_l)))
    if len(con_l) > 0:
        return render_to_response(
            'deletesupervisor.html',
            {'supcontacts': con_l},
            context_instance=RequestContext(request)
        )#
    else:
        del_contact = Contact.objects.get(id=con_id)
        logger.debug("deleting contact")
        logger.debug( con.first_name)
        del_contact.delete()
        logger.debug("deleted contact")
        return render_to_response(
            'contactdelete.html',
            {'contactid': con_id,'user':request.user},
            context_instance=RequestContext(request)
        )#

def editcontactform(request,con_id):
    #if (request.user.is_authenticated() == False):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    logger.debug("this is edit contact form")
    document = Contact.objects.get(id=con_id)
    # Handle file upload
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            picture1 = request.FILES['picture']
            c_id = request.POST['c_id']
            old_pic1 = request.POST['old_pic']
            last_name1 = request.POST['last_name']
            first_name1 = request.POST['first_name']
            sur_name1 = request.POST['sur_name']
            log_name1 = request.POST['log_name']
            email1 = request.POST['email']
            emp_id1 = request.POST['emp_id']
            phone1 = request.POST['phone']
            supervisor1 = request.POST['supervisor']
            jobtitle1 = request.POST['title']
            department1 = request.POST['department']
            H_No1 = request.POST['H_No']
            Line_1 = request.POST['Line1']
            street1 = request.POST['street']
            colony1 = request.POST['colony']
            city1 = request.POST['city']
            pin1 = request.POST['pin']
            add1 = Address(H_No=H_No1,Line1=Line_1,street=street1,colony=colony1,city=city1,pin=pin1)
            add1.save()
            pin1 = request.POST['pin']
            sup1 = Supervisor.objects.filter(sup_id=supervisor1)[0]
            job1 = JobTitle.objects.filter(title=jobtitle1)[0]
            #dep1 = Department.objects.filter(dep_name=department1)[0]
            dep1 = Department.objects.get(id=department1)
            con_obj = Contact.objects.get(id=c_id)
            if sup1 and job1 and dep1:
               #newdoc = Contact(first_name=first_name1,last_name=last_name1,sur_name=sur_name1,email=email1,emp_id=emp_id1,supervisor=sup1,department=dep1,job_title=job1,phone=phone1,picture=picture1,address=add1)
               #newdoc.save()
               con_obj.first_name = first_name1
               con_obj.last_name = last_name1
               con_obj.sur_name = sur_name1
               con_obj.login_name = log_name1
               con_obj.email = email1
               con_obj.emp_id = emp_id1
               con_obj.supervisor = sup1
               # remove existing department for the period
               for de in con_obj.department.filter(from_year=dep1.from_year, to_year=dep1.to_year):
                   #con_obj.department.remove(de)
                   de.contact_set.remove(con_obj)
                   logger.debug("delete dep %s"%de.dep_name)
               con_ob = Contact.objects.get(id=c_id)
               con_ob.department.add(dep1)
               con_ob.save()
               con_obj.job_title = job1
               con_obj.phone = phone1
               con_obj.address = add1
               if picture == None:
                  con_obj.picture = old_pic1
               else:
                  con_obj.picture = picture1 
               con_obj.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('modelsapp.views.editcontact'))
    else:
        default_data={'c_id':document.id,'old_pic':document.picture,'picture':document.picture,'first_name':document.first_name,'last_name':document.last_name,'sur_name':document.sur_name,'log_name':document.login_name,'email':document.emp_id,'phone':document.phone,'email':document.email,'emp_id':document.emp_id,'H_No':document.address.H_No,'Line1':document.address.Line1,'street':document.address.street,'colony':document.address.colony,'city':document.address.city,'pin':document.address.pin}
        form = ContactForm(default_data) 

    # Load documents for the list page
    #documents = Document.objects.all()
    supervisors = Supervisor.objects.all()
    jobtitle = JobTitle.objects.all()
    department = Department.objects.all()
    users_list = User.objects.all()
    f_year = datetime.datetime.today().year
    t_year = int(f_year) + 1
    co = Contact.objects.get(id=con_id)
    department_name = "No Department"
    #dep = co.department.filter(from_year=f_year,to_year=t_year)
    #if dep == None or len(dep) < 1:
    #   department_name = "No Department"
    #else:
    #   department_name = dep[0].dep_name
    #users_list = []

    # Render list page with the documents and the form
    return render_to_response(
        'econtactform.html',
        #{'documents': documents, 'form': form},
        {'form': form,'supervisors':supervisors,'jobtitle':jobtitle,'department':department,'supervisor_id':document.supervisor.sup_id, 'jobtitle_name':document.job_title.title, 'department_name':department_name,'picture':document.picture,'user':request.user,  'user_list':users_list},
        context_instance=RequestContext(request)
    )#

def viewcontact(request,con_id):
    #if (request.user.is_authenticated() == False):
    if request.user.is_authenticated():
        logger.debug ("request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)

    document = Contact.objects.get(id=con_id)
    """
    f_year = datetime.datetime.today().year
    t_year = int(f_year) + 1 
    dep = document.department.filter(from_year=f_year,to_year=t_year)
    dep_name = dep[0].dep_name
    """
    dep = document.department.filter(ac_year__current = True)

    return render_to_response(
         'viewcontact2.html',
         {'document': document,'department_name':dep[0].dep_name},
         #{'form': form},
         context_instance=RequestContext(request)
    )#

def supervisorform(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    # Handle file upload
    if request.method == 'POST':
        form = SupervisorForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Supervisor(sup_id = request.POST['sup_id'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('modelsapp.views.supervisorform'))
    else:
        form = SupervisorForm() # A empty, unbound form

    # Load documents for the list page
    documents = Supervisor.objects.all()
    contacts = Contact.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'supervisor.html',
        {'supervisor': documents, 'form': form, 'contacts':contacts,'user':request.user},
        #{'form': form},
        context_instance=RequestContext(request)
    )#

def deletesearchform(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    if request.method == 'POST':
        form = ESearchForm(request.POST, request.FILES)
        if form.is_valid():
            search_key = request.POST['search_key']
            documents0 = list(Contact.objects.filter(first_name__contains=search_key))
            documents1=list(Contact.objects.filter(last_name__contains=search_key))
            for doc in documents1:
                documents0.append(doc)
            documents2=list(Contact.objects.filter(sur_name__contains=search_key))
            for doc in documents2:
                documents0.append(doc)
            contact_id_list = []
            for doc in documents0:
               if contact_id_list.__contains__(doc.id):
                 pass
               else:
                  contact_id_list.append(doc.id)
            documents = []
            for con_id in contact_id_list:
                con_ob = Contact.objects.get(id=con_id)
                documents.append(con_ob)
            # Redirect to the document list after POST
            #return HttpResponseRedirect(reverse('modelsapp.views.esearchform'))
    else:
        form = ESearchForm() # A empty, unbound form
        documents = None

    # Load documents for the list page
    #documents = Department.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'dsearch.html',
        {'search': documents, 'form': form,'user':request.user},
        #{'form': form},
        context_instance=RequestContext(request)
    )#

def editsearchform(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    if request.method == 'POST':
        form = ESearchForm(request.POST, request.FILES)
        if form.is_valid():
            search_key = request.POST['search_key']
            documents0 = list(Contact.objects.filter(first_name__contains=search_key))
            documents1=list(Contact.objects.filter(last_name__contains=search_key))
            for doc in documents1:
                documents0.append(doc)
            documents2=list(Contact.objects.filter(sur_name__contains=search_key))
            for doc in documents2:
                documents0.append(doc)
            contact_id_list = []
            for doc in documents0:
               if contact_id_list.__contains__(doc.id):
                 pass
               else:
                  contact_id_list.append(doc.id)
            documents = []
            for con_id in contact_id_list:
                con_ob = Contact.objects.get(id=con_id)
                documents.append(con_ob)
            # Redirect to the document list after POST
            #return HttpResponseRedirect(reverse('modelsapp.views.esearchform'))
    else:
        form = ESearchForm() # A empty, unbound form
        documents = None

    # Load documents for the list page
    #documents = Department.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'esearch.html',
        {'search': documents, 'form': form, 'user':request.user},
        #{'form': form},
        context_instance=RequestContext(request)
    )#
def skillsearchform(request):
    if request.user.is_authenticated():
        logger.debug ("request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    if request.method == 'POST':
        search_key = request.POST['title']
        co_list = Contact.objects.filter(skill__skill_name__contains=search_key)
    else:
        co_list = None
    tit_list = SkillTitle.objects.all() 
    logger.debug ("request user %d is authenticated"%len(tit_list))
    return render_to_response(
                 'skillsearch.html',
                  {'search': co_list,'title_list':tit_list, 'user':request.user},
                  context_instance=RequestContext(request)
    )#
     
def esearchform(request):
    if request.user.is_authenticated():
        logger.debug ("request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    if request.method == 'POST':
        form = ESearchForm(request.POST, request.FILES)
        if form.is_valid():
            search_key = request.POST['search_key']
            documents0 = list(Contact.objects.filter(first_name__contains=search_key))
            documents1=list(Contact.objects.filter(last_name__contains=search_key))
            for doc in documents1:
                documents0.append(doc)
            documents2=list(Contact.objects.filter(sur_name__contains=search_key))
            for doc in documents2:
                documents0.append(doc)
            contact_id_list = []
            for doc in documents0:
               if contact_id_list.__contains__(doc.id):
                 pass
               else:
                  contact_id_list.append(doc.id)
            documents = []
            for con_id in contact_id_list:
                con_ob = Contact.objects.get(id=con_id)
                documents.append(con_ob)
            # Redirect to the document list after POST
            #return HttpResponseRedirect(reverse('modelsapp.views.esearchform'))
    else:
        form = ESearchForm() # A empty, unbound form
        documents = None

    # Load documents for the list page
    #documents = Department.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'search.html',
        {'search': documents, 'form': form},
        #{'form': form},
        context_instance=RequestContext(request)
    )#

def departmentform(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    # Handle file upload
    message =""
    logger.debug("department form")
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            logger.debug(form.is_valid())
            dep_name_var = request.POST['dep_name']
            class_teacher_id_var=request.POST['class_teacher_id']
            """
            from_year_var=request.POST['from_year']
            to_year_var=request.POST['to_year']
            """
            ay_id=request.POST['academic_year']
            ay = AcademicYear.objects.get(id = ay_id)
            #newdoc = Department(dep_name = dep_name_var,class_teacher_id=class_teacher_id_var,from_year=from_year_var,to_year=to_year_var)
            de_list = ay.department_set.filter(dep_name = dep_name_var)
            if len( de_list ) < 1:
                newdoc = Department(dep_name = dep_name_var,class_teacher_id=class_teacher_id_var)
                newdoc.save()
            else:
               message = str("Duplicate Department, Hence not saved")
            """
            newdoc = Department(dep_name = dep_name_var,class_teacher_id=class_teacher_id_var)
            try:
               newdoc.full_clean()
            except ValidationError as e:
               message = str("Duplicate Department, Hence not saved")
            """
            if ( message == ""):
               #newdoc.save()
               ay.department_set.add(newdoc)
               message = str("Department Saved")
               form = DepartmentForm() # A empty, unbound form
            documents = Department.objects.all()
            ay_list = AcademicYear.objects.all()

            return render_to_response(
                 'department.html',
                  {'department': documents, 'form': form,'user':request.user, "msg":message, 'ay_list':ay_list},
                  context_instance=RequestContext(request)
            )#

            # Redirect to the document list after POST
            #return HttpResponseRedirect(reverse('modelsapp.views.departmentform'))
    else:
        form = DepartmentForm() # A empty, unbound form

    # Load documents for the list page
    a_list = AcademicYear.objects.filter(current = True)
    documents = a_list[0].department_set.all()
    #documents = Department.objects.all()
    ay_list = AcademicYear.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'department.html',
        {'department': documents, 'form': form,'user':request.user, "msg":message,'ay_list':ay_list},
        context_instance=RequestContext(request)
    )#


def jobtitleform(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    # Handle file upload
    if request.method == 'POST':
        form = JobTitleForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = JobTitle(title = request.POST['title'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('modelsapp.views.jobtitleform'))
    else:
        form = JobTitleForm() # A empty, unbound form

    # Load documents for the list page
    documents = JobTitle.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'jobtitle.html',
        {'jobtitle': documents, 'form': form,'user':request.user},
        #{'form': form},
        context_instance=RequestContext(request)
    )#

def addacademicyear(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("request user %s is authenticated"%request.user.username)
    else:
        logger.debug ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    # Handle file upload
    if request.method == 'POST':
        form = AddAcademicYearForm(request.POST)
        #if form.is_valid():
        if request.POST.has_key('academic_year'):
               logger.debug(" ay id ")
               newdoc = AcademicYear(academic_year = request.POST['academic_year'])
               newdoc.save()
        if request.POST.has_key('current'):
                 logger.debug(" current  ")
                 ay_list = AcademicYear.objects.filter(current = True)
                 for ay_obj in ay_list:
                    ay_obj.current = False
                    ay_obj.save()
                 ay_id = request.POST['current']
                 ay = AcademicYear.objects.get(id = ay_id)
                 logger.debug(" ay id %d"%int(ay_id))
                 ay.current = True
                 ay.save()

            # Redirect to the document list after POST
        return HttpResponseRedirect(reverse('modelsapp.views.addacademicyear'))
    else:
        form = AddAcademicYearForm() # A empty, unbound form

    # Load documents for the list page
    #documents = AcademicYear.objects.all()
    documents = AcademicYear.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'academicyear.html',
        {'jobtitle': documents, 'form': form,'user':request.user},
        #{'form': form},
        context_instance=RequestContext(request)
    )#
def login(request):
    c={}
    c.update(csrf(request))
    return render_to_response("login.html",c)
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/Contacts/login/")
    #auth_logout(request)


def adminindex(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password= password)
        if user.is_active:
            logger.error ( "error message use rname " + request.user.username)
            logger.debug ( "debug message use rname " + request.user.username)
            auth_login(request, user)
        else:
            logger.debug ( " rname " + request.user.username)
    return render_to_response(
            'adminindex.html',
            {'user':request.user},
            context_instance=RequestContext(request)
    )
    """
    if user.is_superuser:
        return render_to_response(
            'adminindex.html',
            {'user':request.user},
            context_instance=RequestContext(request)
        )
    else:
        return render_to_response(
            'userindex.html',
            {},
            context_instance=RequestContext(request)
        )
    """
def subjecttodep(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("debug request user %s is authenticated"%request.user.username)
        logger.error ("error request user %s is authenticated"%request.user.username)
    else:
        logger.error ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    logger.debug ("subjecttodep form")
    message=""
    if request.method == 'POST':
       dep_id = request.POST['department'] 
       dep = Department.objects.get(id = dep_id)
       for key in request.POST.keys():
          logger.debug("key %s"%key)
          key_list = key.split("ck_")
          if len(key_list) > 1:
              logger.debug("key list :%s:"%key_list[-1])
              key_id = key_list[-1]
              logger.debug("key list %d"%int(key_id))
              sub = Subject.objects.get(id = int(key_list[-1].strip()))
              sub.department.add(dep)
       ay_list = AcademicYear.objects.filter(current = True)
       department_list = ay_list[0].department_set.all()
       subject_list = ay_list[0].subject_set.all()
    else:
       ay_list = AcademicYear.objects.filter(current = True)
       if len(ay_list) > 1:
           message = str("Error(Multiple Current Academic year) in getting current academic year")
           department_list = [] 
           subject_list = []
       else:
           department_list = ay_list[0].department_set.all()
           subject_list = ay_list[0].subject_set.all()
       
    return render_to_response(
        'subjecttodep.html',
        {'user':request.user, 'msg':message, 'department':department_list,'subject':subject_list},
        context_instance=RequestContext(request)
    )#

def edittest(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("debug request user %s is authenticated"%request.user.username)
        logger.error ("error request user %s is authenticated"%request.user.username)
    else:
        logger.error ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    logger.debug ("edit test form")
    message = str("")
    if request.method == 'POST':
       ay_lis = AcademicYear.objects.filter(current = True)
       test_list = ay_lis[0].test_set.all()
       logger.debug("len %d"%len(test_list))
       test_name_list = []
       for test in test_list:
           logger.debug(test.test_name)
           test_name_list.append(test.test_name)
       test_name_set = set(test_name_list)
       test_name_unique_list = list(test_name_set)
       form_id_str = str("")
       form_dep_id = None
       form_sub_id = None
       form_test_str = str("")
       for test_name_uni in test_name_unique_list:
           for dep in Department.objects.all(): 
               for sub in Subject.objects.all():
                    id_str = str(test_name_uni) + str("^") + str(sub.id) + str("^") + str(dep.id)
                    if request.POST.has_key(id_str):
                        form_id_str = id_str
                        form_dep_id = dep.id
                        form_test_str = test_name_uni
                        form_sub_id = sub.id
                    pass
               pass
           pass
       pass
       department = None
       subject = None
       if form_id_str != "":
           message = form_id_str
           department = Department.objects.get(id = form_dep_id)
           subject = Subject.objects.get(id = form_sub_id)
       context={'user':request.user, 'msg':message, 'te_name':form_test_str, 'dep_id':form_dep_id,"sub_id":form_sub_id, "ay":ay_lis[0], "dept":department,"subt":subject}
       context.update(csrf(request))
       return render_to_response(
              'edittest.jinja',
              context,
       )#
    else:
       context={'user':request.user, 'msg':message }
       context.update(csrf(request))
       return render_to_response(
              'edittest_new.jinja',
              context,
       )#
          

def reportcard(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("debug request user %s is authenticated"%request.user.username)
        logger.error ("error request user %s is authenticated"%request.user.username)
    else:
        logger.error ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    logger.debug ("report card form")
    ay_list = AcademicYear.objects.filter(current = True)
    con_list = ay_list[0].contact_set.filter(login_name = request.user.username)
    logger.debug ("con_list len %d "%len(con_list))
    contact = None
    dep = None
    test_name_unique_list = []
    message = str("")
    if request.method == 'POST':
        con_id = request.POST["contact_id"]
        contact = Contact.objects.get(id = con_id)
        dep_list = contact.department.filter(ac_year = ay_list[0])
        test_name_list = []
        for tes in contact.test_set.all():
            test_name_list.append(tes.test_name)
        test_name_set = set(test_name_list)
        test_name_unique_list = list(test_name_set)
        dep = dep_list[0]
    context={'user':request.user, 'msg':message, 'contact_list':con_list, 'cont':contact,"department":dep, "test_list":test_name_unique_list, "ay":ay_list[0]}
    context.update(csrf(request))
    return render_to_response(
        'reportcard.jinja',
         context,
    )#


def viewtest(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("debug request user %s is authenticated"%request.user.username)
        logger.error ("error request user %s is authenticated"%request.user.username)
    else:
        logger.error ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    logger.debug ("view test form")
    message = str("")
    #message=str(django.get_version())
    #message=str("test123")
    #ay_list = AcademicYear.objects.filter(current = True)
    dep = None
    test_list = []
    ay_list = AcademicYear.objects.filter(current = True)
    logger.debug(ay_list[0].academic_year)
    dep_list = ay_list[0].department_set.all()
    test_list = ay_list[0].test_set.all()
    logger.debug("len %d"%len(test_list))
    test_name_list = []
    for test in test_list:
        logger.debug(test.test_name)
        test_name_list.append(test.test_name)
    test_name_set = set(test_name_list)
    test_name_unique_list = list(test_name_set)
    test_name_var = str("")
    if request.method == 'POST':
       if request.POST.has_key('edit_test'):
           edit_test_name_var = str("")
           te_uni = str("")
           su_id = None
           de_id = None
           for test_name_uni in test_name_unique_list:
               for de in Department.objects.all():
                   for su in Subject.objects.all():
                       edit_test_name_var = str(test_name_uni)+str("^")+str(su.id)+str("^")+str(de.id)
                       if request.POST.has_key(edit_test_name_var):
                           te_uni = test_name_uni
                           su_id = su.id
                           de_id = de.id
           dep_sel = Department.objects.get(id = de_id)
           sub_sel = Subject.objects.get(id = su_id)
           marks_str = str("")
           grade_str = str("")
           comments_str = str("")
           for con_sel in dep_sel.contact_set.all():
                for tes in ay_list[0].test_set.filter(test_name = te_uni, subject = sub_sel, contact = con_sel):
                   marks_str = str(te_uni)+ str("^")+str(sub_sel.id)+str("^")+str(con_sel.id)+str("^marks")
                   grade_str = str(te_uni)+ str("^")+str(sub_sel.id)+str("^")+str(con_sel.id)+str("^grade")
                   comments_str = str(te_uni)+ str("^")+str(sub_sel.id)+str("^")+str(con_sel.id)+str("^comment")
                   marks_val = request.POST[marks_str]
                   grade_val = request.POST[grade_str]
                   comments_val = request.POST[comments_str]
                   tes.marks = marks_val
                   tes.grade = grade_val
                   tes.comment = comments_val
                   tes.save()
           pass
       else:
          ay_lis = AcademicYear.objects.filter(current = True)
          dep_id_var = request.POST['department']
          test_name_var = request.POST['test']
          dep = Department.objects.get(id = dep_id_var)
          #contacts_list = Department.contact_set.all()
          test_list = ay_lis[0].test_set.all()
    #context=RequestContext(request)
    #for k in request.keys():
    #     logger.debug("key => %k"%k)
    context={'user':request.user, 'msg':message, 'd_list':dep_list, 't_list':test_name_unique_list,"department":dep, "test_list":test_list, "ay":ay_list[0], "te_name":test_name_var}
    context.update(csrf(request))
    return render_to_response(
        'viewtest.jinja',
         context,
    )#

def addtest(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("debug request user %s is authenticated"%request.user.username)
        logger.error ("error request user %s is authenticated"%request.user.username)
    else:
        logger.error ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    logger.debug ("test form")
    message=""
    ay_list = AcademicYear.objects.filter(current = True)
    if request.method == 'POST':
            dep_id_var = request.POST['department']
            test_name_var = request.POST['test_name']
            dep = Department.objects.get(id = dep_id_var)
            test_flag = True 
            for con in dep.contact_set.all():
                test_list =  con.test_set.filter(test_name = test_name_var)
                if len(test_list) > 0:
                    message = str("Test already Added")
                    test_flag = False
            if test_flag:
                dep = Department.objects.get(id = dep_id_var)
                for con in dep.contact_set.all():
                    for sub in  dep.subject_set.all():
                         test = Test(test_name = test_name_var, marks = 0, grade="NA", comment = "Not Entered")
                         test.save()
                         logger.debug("test added %s"%test_name_var)
                         sub.test_set.add(test)
                         con.test_set.add(test)
                         logger.debug(ay_list[0].academic_year)
                         ay_list[0].test_set.add(test)
                         for  te in ay_list[0].test_set.all():
                             logger.debug("test %s"%te.test_name)
                message = str("Test Added")
            dep_list = ay_list[0].department_set.all()
    else:
       if len(ay_list) > 1:
            message = str("Multiple current years found")
            #dep_list = Department.objects.all()
            dep_list = []
       else:
           dep_list = ay_list[0].department_set.all()
    return render_to_response(
        'addtest.html',
        {'user':request.user, 'msg':message, 'department':dep_list},
        context_instance=RequestContext(request)
    )#

def addsubject(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("debug request user %s is authenticated"%request.user.username)
        logger.error ("error request user %s is authenticated"%request.user.username)
    else:
        logger.error ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    logger.debug ("addsubject form")
    message=""
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        logger.debug (form.is_valid())
        if form.is_valid():
            sub_name_var = request.POST['sub_name']
            teacher_id_var = request.POST['teacher_id']
            text_book_var = request.POST['text_book']
            publisher_var = request.POST['publisher']
            """
            from_year_var = request.POST['from_year']
            to_year_var = request.POST['to_year']
            """
            dep_id_var = request.POST['department']
            ay_id_var = request.POST['academic_year']
            dep=Department.objects.get(id=dep_id_var)
            ay=AcademicYear.objects.get( id = ay_id_var)
            su_list = ay.subject_set.filter(sub_name = sub_name_var, teacher_id = teacher_id_var, text_book = text_book_var, department_name=dep.dep_name)
            if len(su_list ) < 1:
                 #sub = Subject(sub_name=sub_name_var,teacher_id=teacher_id_var,text_book=text_book_var,publisher=publisher_var,from_year=from_year_var,to_year=to_year_var,department_name=dep.dep_name)
                 sub = Subject(sub_name=sub_name_var,teacher_id=teacher_id_var,text_book=text_book_var,publisher=publisher_var,department_name=dep.dep_name)
                 sub.save()
            else:
                 message = str("Duplicate Subject, Hence not Added")
            """
            try:
              sub.full_clean()
            except ValidationError as e:
              message = str("Duplicate Subject, Hence not Added")
            """
            if ( message == "" ):
               dep=Department.objects.get(id=dep_id_var)
               logger.debug ("department name %s"%dep.dep_name)
               #sub.save()
               sub.department.add(dep)
               ay.subject_set.add(sub)
               #sub.save()
               message=str("Subject Added")
            form = SubjectForm() # A empty, unbound form
    else:
        form = SubjectForm() # A empty, unbound form
    department = Department.objects.all()
    #department_list = Department.objects.all()
    a_list = AcademicYear.objects.filter(current = True)
    department_list = a_list[0].department_set.all()
    subject_list = Subject.objects.all()
    jt=JobTitle.objects.filter(title='Teacher')
    t_list = jt[0].contact_set.all()
    ay_list = AcademicYear.objects.all()
       
    return render_to_response(
        'subject.html',
        {'form': form,'user':request.user, 'msg':message, 'department':department_list,'subject':subject_list,'teachers_list':t_list,'ay_list':ay_list},
        context_instance=RequestContext(request)
    )#
            
def searchsubject(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("debug request user %s is authenticated"%request.user.username)
        logger.error ("error request user %s is authenticated"%request.user.username)
    else:
        logger.error ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)

def editsubject(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("debug request user %s is authenticated"%request.user.username)
        logger.error ("error request user %s is authenticated"%request.user.username)
    else:
        logger.error ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    message=""
    if request.method == 'POST':
       subjects_list = Subject.objects.all()
       for subj in subjects_list:
            key_str= str("sub_name_") + str(subj.id)
            #key_from_year= str("from_year_") + str(subj.id)
            #key_to_year= str("to_year_") + str(subj.id)
            key_dep_id= str("dep_") + str(subj.id)
            key_teacher_id= str("teacher_") + str(subj.id)
            key_text_book_id= str("text_book_") + str(subj.id)
            key_publisher_id= str("publisher_") + str(subj.id)
            #key_ay_id= str("academic_year_") + str(subj.id)
            if (request.POST.has_key(key_str) and request.POST.has_key(key_text_book_id) and request.POST.has_key(key_publisher_id) and request.POST.has_key(key_teacher_id) ):
                s_name = request.POST[key_str]
                #f_year = request.POST[key_from_year]
                #t_year = request.POST[key_to_year]
                #dep_id = request.POST[key_dep_id]
                #ay_id = request.POST[key_ay_id]
                teacher_id = request.POST[key_teacher_id]
                text_book_var = request.POST[key_text_book_id]
                publisher_var = request.POST[key_publisher_id]
                teacher_id = request.POST[key_teacher_id]
                sub_obj = Subject.objects.get( id = subj.id) 
                #dep = sub_obj.department.get(from_year = sub_obj.from_year, to_year = sub_obj.to_year)
                #sub_obj.from_year = f_year
                #sub_obj.to_year = t_year
                sub_obj.sub_name = s_name
                sub_obj.teacher_id = teacher_id
                sub_obj.publisher = publisher_var
                sub_obj.text_book = text_book_var
                sub_obj.save()
                #dep.subject_set.remove( sub_obj )
                logger.debug ("old Dep id %d"%dep.id)
                #dep.save()
                #dep_id_list = dep_id.split('_')
                #logger.debug ("new Dep id %d"%int(dep_id_list[-1]))
                #dep_new = Department.objects.get( id = dep_id_list[-1] )
                #dep_new.subject_set.add( sub_obj )
                #dep_new.save()
                message = str("Subject Updated")
    form = SubjectForm() # A empty, unbound form
    department_list = Department.objects.all()
    subject_list = Subject.objects.all()
    jt=JobTitle.objects.filter(title='Teacher')
    t_list = jt[0].contact_set.all()
       
    return render_to_response(
        'subject.html',
        {'form': form,'user':request.user, 'msg':message, 'department':department_list,'subject':subject_list,'teachers_list':t_list},
        context_instance=RequestContext(request)
    )#

def contactform(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug ("debug request user %s is authenticated"%request.user.username)
        logger.error ("error request user %s is authenticated"%request.user.username)
    else:
        logger.error ("request user %s is authenticated"%request.user.username)
        c={}
        c.update(csrf(request))
        return render_to_response("login.html",c)
    # Handle file upload
    logger.debug ("contact form")
    if request.method == 'POST':
        logger.debug ("contact form1")
        logger.debug ("contact form1")
        form = ContactForm(request.POST, request.FILES)
        logger.debug (form.is_valid())
        academic_year_flag = False
        if form.is_valid():
            logger.debug ("contact form2")
            picture1 = request.FILES['picture']
            c_id = request.POST['c_id']
            old_pic1 = request.POST['old_pic']
            last_name1 = request.POST['last_name']
            first_name1 = request.POST['first_name']
            sur_name1 = request.POST['sur_name']
            log_name1 = request.POST['log_name']
            logger.debug ("contact form2 %s"% (log_name1))
            email1 = request.POST['email']
            emp_id1 = request.POST['emp_id']
            phone1 = request.POST['phone']
            supervisor1 = request.POST['supervisor']
            jobtitle1 = request.POST['title']
            department1 = request.POST['department']
            if request.POST.has_key('academic_year'):
               academic_year_flag = True
               ay_id = request.POST['academic_year']
            H_No1 = request.POST['H_No']
            Line_1 = request.POST['Line1']
            street1 = request.POST['street']
            colony1 = request.POST['colony']
            city1 = request.POST['city']
            pin1 = request.POST['pin']
            add1 = Address(H_No=H_No1,Line1=Line_1,street=street1,colony=colony1,city=city1,pin=pin1)
            add1.save()
            pin1 = request.POST['pin']
            sup1 = Supervisor.objects.filter(sup_id=supervisor1)[0]
            job1 = JobTitle.objects.filter(title=jobtitle1)[0]
            #dep1 = Department.objects.filter(dep_name=department1)[0]
            dep1 = Department.objects.get(id=department1)
            if ( academic_year_flag ):
               ay1 = AcademicYear.objects.get(id=ay_id)
            logger.debug (c_id)
            logger.debug ("old_pic1 " + str(old_pic1))
            if ((int(c_id) == 0) and (old_pic1 == '0')):
               logger.debug ("new contact saving")
               #newdoc = Contact(first_name=first_name1,last_name=last_name1,sur_name=sur_name1,login_name=log_name1,email=email1,emp_id=emp_id1,supervisor=sup1,department=dep1,job_title=job1,phone=phone1,picture=picture1,address=add1)
               newdoc = Contact(first_name=first_name1,last_name=last_name1,sur_name=sur_name1,login_name=log_name1,email=email1,emp_id=emp_id1,supervisor=sup1,job_title=job1,phone=phone1,picture=picture1,address=add1)
               newdoc.save()
               newdoc.department.add(dep1)
               if ( academic_year_flag ):
                   ay1.contact_set.add(newdoc)
               ay_list = AcademicYear.objects.filter(current = True)
               #TODO:DONE get testlist for the department
               #
               te_name_list = []
               for ct in dep1.contact_set.all():
                   for te in ct.test_set.filter(academic_year__current = True):
                       te_name_list.append(te.test_name)
               te_name_set = set(te_name_list)
               te_name_unique_list = list(te_name_set)
               """
               test_list = ay_list[0].test_set.all()
               logger.debug("len %d"%len(test_list))
               test_name_list = []
               for test in test_list:
                   logger.debug(test.test_name)
                   test_name_list.append(test.test_name)
               test_name_set = set(test_name_list)
               test_name_unique_list = list(test_name_set)
               """
               test_name_unique_list = te_name_unique_list
               for su in dep1.subject_set.all():
                    for te_name in test_name_unique_list:
                        tes = Test(test_name = te_name, marks = 0, grade="NA", comment = "Not Entered")
                        tes.save()
                        su.test_set.add(tes)
                        newdoc.test_set.add(tes)
                        ay_list[0].test_set.add(tes)
            elif ((int(c_id) > 0)):
               logger.debug ("edited contact saving")
               con_obj = Contact.objects.get(id=c_id)
               con_obj.first_name = first_name1
               con_obj.last_name = last_name1
               con_obj.sur_name = sur_name1
               con_obj.login_name = log_name1
               con_obj.email = email1
               con_obj.emp_id = emp_id1
               con_obj.supervisor = sup1
               #con_obj.department = dep1
               con_obj.job_title = job1
               con_obj.phone = phone1
               con_obj.address = add1
               if picture1 == None:
                  con_obj.picture = old_pic1
               else:
                  con_obj.picture = picture1
               logger.debug("edit contact saving =>  %s"%log_name1)
               a_list = AcademicYear.objects.filter(current = True)
               dep1
               for de in con_obj.department.filter(ac_year__current=True):
                   #con_obj.department.remove(de)
                   de.contact_set.remove(con_obj)
               con_obj.department.add(dep1)
               con_obj.save()
               logger.debug("edit contact saving =>  %s"%con_obj.login_name)


            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('modelsapp.views.contactform'))
    else:
        default_data={'c_id':0,'old_pic':'0'}
        form = ContactForm(default_data) # A empty, unbound form

    # Load documents for the list page
    #documents = Document.objects.all()
    supervisors = Supervisor.objects.all()
    jobtitle = JobTitle.objects.all()
    department = Department.objects.all()
    users_list = User.objects.all()
    ay_list = AcademicYear.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'contactform.html',
        #{'documents': documents, 'form': form},
        {'form': form,'supervisors':supervisors,'jobtitle':jobtitle,'department':department,'user':request.user, 'user_list':users_list,'ay_list':ay_list},
        context_instance=RequestContext(request)
    )#

