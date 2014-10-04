# controller utama

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User

def bulan_ini():
    import time
    tgl = time.strftime("%d/%m/%Y")
    bulan = tgl[4:6]
    return bulan


def tgl2db(tgl):
    glue=''
    sec = (tgl[6:],tgl[3:5],tgl[:2])
    tgl = glue.join(sec)
    return tgl

def db2tgl(tgl):
    if tgl:
        garing = '/'
        sec = (tgl[6:],tgl[4:6],tgl[:4])
        tgl = garing.join(sec)
        return tgl
    else:
        return tgl

def db2tanggal(tgl):
    garing = ' '
    bulan = tgl[4:6]
    if bulan=='01':
        bulan='Januari'
    else:
        if bulan=='02':
            bulan='Februari'
        else:
            if bulan=='03':
                bulan='Maret'
            else:
                if bulan=='04':
                    bulan='April'
                else:
                    if bulan=='05':
                        bulan='Mei'
                    else:
                        if bulan=='06':
                            bulan='Juni'
                        else:
                            if bulan=='07':
                                bulan='Juli'
                            else:
                                if bulan=='08':
                                    bulan='Agustus'
                                else:
                                    if bulan=='09':
                                        bulan='September'
                                    else:
                                        if bulan=='10':
                                            bulan='Oktober'
                                        else:
                                            if bulan=='11':
                                                bulan='November'
                                            else:
                                                if bulan=='12':
                                                    bulan='Desember'
    sec = (tgl[6:],bulan,tgl[:4])
    tgl = garing.join(sec)
    return tgl

def index(request):
    if request.user.is_authenticated():
        context=RequestContext(request)
        from main.models import Hardware, User, Tindakan, Lokasi, Kathw
        current_user = request.user.get_username()
        tindakan_list = Tindakan.objects.filter(status='Proses')
        for x in tindakan_list:
            x.short_title = x.masalah
        from main.models import Kanban
        gtd_data = Kanban.objects.all()
        import jsonpickle, json
        i=0
        gtd_array = {}
        for y in gtd_data:
            gtd_array[i]= {}
            gtd_array[i]['noid_tin'] = y.noid_tin.noid_tin
            gtd_array[i]['noid_kanban'] = y.noid_kanban
            gtd_array[i]['urut'] = y.urut
            gtd_array[i]['owner'] = y.owner
            i=i+1
        gtd = json.dumps(gtd_array)

        context_dict = {'tindakan_list' : tindakan_list, 'gtd' : gtd, 'current_user' : current_user}

        return render_to_response('main/kanban.html', context_dict, context)
    else :
        return HttpResponseRedirect("/main/login")

def gtd_get_json(request):
    if request.user.is_authenticated():
        context=RequestContext(request)
        from main.models import Kanban
        data = Kanban.objects.filter(archived='0')
        from django.core import serializers
        gtd_data = serializers.serialize('json', data)
        return HttpResponse(gtd_data, mimetype="application/json")

def gtd_post_kanban_update(request):
        if request.user.is_authenticated():
            context=RequestContext(request)
            from main.models import Kanban, Tindakan
            if request.method == 'GET':
                if request.GET['slot'] == 'done':
                    idnya = request.GET['idnya']
                    slot = request.GET['slot']
                    item = Kanban.objects.filter(noid_tin = idnya).get()
                    item.slot = slot
                    item.archived = '1'
                    item.delete()
                    item.save()

                    tindakan = Tindakan.objects.filter(noid_tin = idnya).get()
                    tindakan.status = 'Selesai'
                    tindakan.save()

                    return HttpResponse('OK')
                else :
                    idnya = request.GET['idnya']
                    slot = request.GET['slot']
                    item = Kanban.objects.filter(noid_tin = idnya).get()
                    item.slot = slot
                    item.archived = '0'
                    item.save()

                    tindakan = Tindakan.objects.filter(noid_tin = idnya).get()
                    tindakan.status = 'Proses'
                    tindakan.save()
                    return HttpResponse('OK')


def tindakan(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            tanggal_buka = tgl2db(request.POST['tanggal_buka'])


            noid_hw = request.POST['noid_hw']
            masalah = request.POST['masalah']
            penyelesaian = request.POST['penyelesaian']
            jenis_tindakan = request.POST['jenis_tindakan']
            status = request.POST['status']
            import time
            time_create = time.time()

            noid_hw_split=noid_hw.split(" |")
            noid_hw=noid_hw_split[0]

            from main.models import Hardware, User, Tindakan, Lokasi, Kathw, Kanban
            username=request.user.get_username()
            noid_perangkat=Hardware.objects.get(noid_hw=noid_hw)
            username=User.objects.get(username=username)
            Tindakan.objects.get_or_create(masalah=masalah, penyelesaian=penyelesaian, tanggal_buka=tanggal_buka, jenis_tindakan=jenis_tindakan, status=status, noid_hw=noid_perangkat, username=username, time_create=time_create)
            tin = Tindakan.objects.get(masalah=masalah, penyelesaian=penyelesaian, tanggal_buka=tanggal_buka, jenis_tindakan=jenis_tindakan, status=status, noid_hw=noid_perangkat, username=username, time_create=time_create)
            Kanban.objects.get_or_create(noid_tin=tin, slot='todo', urut=0, owner='piko', archived='0')
            return HttpResponseRedirect("/main/tindakan")
        else:

            context = RequestContext(request)
            from main.models import Hardware, User, Tindakan, Lokasi, Kathw

            if bool(request.GET):

                filter = request.GET['filter']

                if filter == 'status':
                    status = request.GET['status']
                    tindakan_list = Tindakan.objects.filter(status=status).select_related('Hardware').order_by('-tanggal_buka')
                    banyak = 0
                    for y in tindakan_list:
                        y.tanggal_buka = db2tanggal(y.tanggal_buka)
                        banyak = banyak + 1
                    perangkat_list = Hardware.objects.all()
                    kathw_list = Kathw.objects.all()
                    lokasi_list = Lokasi.objects.all()
                    user_list = User.objects.all()
                    current_user = request.user.get_username()
                    context_dict = {'tindakan_list':tindakan_list, 'perangkat_list':perangkat_list,'kathw_list':kathw_list, 'lokasi_list':lokasi_list,'user_list':user_list,'current_user':current_user,'status':status, 'banyak':banyak}

                    return render_to_response('main/tindakan.html', context_dict, context)

            else:

                tindakan_list = Tindakan.objects.all().select_related('Hardware').order_by('-tanggal_buka')
                banyak = 0
                for x in tindakan_list:
                    x.tanggal_buka = db2tanggal(x.tanggal_buka)
                    banyak = banyak + 1


                perangkat_list = Hardware.objects.all()
                kathw_list = Kathw.objects.all()
                lokasi_list = Lokasi.objects.all()
                user_list = User.objects.all()
                current_user = request.user.get_username()
                context_dict = {'tindakan_list':tindakan_list, 'perangkat_list':perangkat_list,'kathw_list':kathw_list, 'lokasi_list':lokasi_list,'user_list':user_list,'current_user':current_user, 'banyak':banyak}

                return render_to_response('main/tindakan.html', context_dict, context)
    else :
        return HttpResponseRedirect("/main/login")

def hapus_tindakan(request):
    if request.user.is_authenticated():
        context=RequestContext(request)
        noid_tin = request.GET['hapus']
        from main.models import Hardware,Tindakan, Lokasi, Kathw, User
        Tindakan.objects.filter(noid_tin=noid_tin).delete()
        return HttpResponseRedirect("/main/tindakan")
    else :
        return HttpResponseRedirect("/main/login")

def hapus_perangkat(request):
    if request.user.is_authenticated():
        context=RequestContext(request)
        noid_hw = request.GET['hapus']
        from main.models import Hardware,Tindakan, Lokasi, Kathw, User
        Hardware.objects.filter(noid_hw=noid_hw).delete()
        return HttpResponseRedirect("../../main/perangkat/")
    else :
        return HttpResponseRedirect("../main/login")

def tindakan_status(request):
    if request.user.is_authenticated():
        context=RequestContext(request)
        status = request.POST['status']
        noid_tin = request.POST['noid_tin']
        masalah = request.POST['masalah']
        # tanggal_buka = request.POST['tanggal_buka']
        tanggal_tutup = request.POST['tanggal_tutup']
        tanggal_tutup = tgl2db(tanggal_tutup)
        penyelesaian = request.POST['penyelesaian']
        from main.models import Hardware,Tindakan, Lokasi, Kathw, User
        tindakan = Tindakan.objects.filter(noid_tin=noid_tin).get()
        tindakan.status=status
        # tindakan.tanggal_buka=tanggal_buka
        tindakan.tanggal_tutup=tanggal_tutup
        tindakan.masalah=masalah
        tindakan.penyelesaian=penyelesaian
        tindakan.save()
        url = ['/main/tindakan_detail/?id=',noid_tin]
        back = ''.join(url)

        return HttpResponseRedirect("/main/tindakan/")
    else :
        return HttpResponseRedirect("/main/login")

def perangkat_detail(request):
    if request.user.is_authenticated():
        context=RequestContext(request)
        noid_hw=request.GET['id']
        from main.models import Hardware, Tindakan, Lokasi, Kathw, User
        perangkat_list = Hardware.objects.filter(noid_hw=noid_hw).select_related('User').select_related('Tindakan')

        for perangkat in perangkat_list:
            noid_hw=perangkat.noid_hw
            merek=perangkat.merek
            tipe=perangkat.tipe
            lokasi=perangkat.lokasi.lokasi
            username=perangkat.username.first_name
            username_=perangkat.username.username
            first_name_=perangkat.username.first_name
            tahun=perangkat.tahun
            kodebrg=perangkat.kodebrg
            keterangan=perangkat.keterangan
            kathw=perangkat.kathw.kathw

        perangkat_list = Hardware.objects.all()
        kathw_list = Kathw.objects.all()
        lokasi_list = Lokasi.objects.all()
        user_list = User.objects.all()

        tindakan_list = Tindakan.objects.filter(noid_hw=noid_hw).all()
        current_user = request.user.get_username()
        context_dict = {
            'noid_hw':noid_hw,
            'merek':merek,
            'tipe':tipe,

            'tahun':tahun,
            'kodebrg':kodebrg,
            'kathw':kathw,
            'lokasi':lokasi,
            'username':username,
            'kathw_':kathw,
            'lokasi_':lokasi,
            'username_':username_,
            'first_name_':first_name_,
            'keterangan':keterangan,
            'tindakan_list':tindakan_list,
            'current_user':current_user,
            'perangkat_list':perangkat_list,
            'kathw_list':kathw_list,
            'lokasi_list':lokasi_list,
            'user_list':user_list,
            }
        return render_to_response('main/perangkat_detail.html', context_dict, context)

    else :
        return HttpResponseRedirect("/main/login")

def tindakan_detail(request):
    if request.user.is_authenticated():
        context=RequestContext(request)
        noid_tin=request.GET['id']
        from main.models import Hardware, Tindakan, Lokasi, Kathw, User
        tindakan_list = Tindakan.objects.filter(noid_tin=noid_tin).select_related('User').select_related('Hardware')

        for tindakan in tindakan_list:
            noid_tin=tindakan.noid_tin
            noid_hw=tindakan.noid_hw.noid_hw
            kathw=tindakan.noid_hw.kathw.kathw
            merek=tindakan.noid_hw.merek
            tipe=tindakan.noid_hw.tipe
            lokasi=tindakan.noid_hw.lokasi.lokasi
            username=tindakan.username.username
            first_name=tindakan.username.first_name
            # tanggal_buka=tindakan.tanggal_buka
            # tanggal_tutup=tindakan.tanggal_tutup
            tanggal_buka=db2tgl(tindakan.tanggal_buka)
            tanggal_tutup=db2tgl(tindakan.tanggal_tutup)
            jenis_tindakan=tindakan.jenis_tindakan
            masalah=tindakan.masalah
            penyelesaian=tindakan.penyelesaian
            status=tindakan.status
            if status=='Proses':
                status_proses=1
            else:
                status_proses=0
            if status=='Tunda':
                status_tunda=1
            else:
                status_tunda=0
            if status=='Batal':
                status_batal=1
            else:
                status_batal=0
            if status=='Selesai':
                status_selesai=1
            else:
                status_selesai=0

        tindakan_list = Tindakan.objects.filter(noid_hw=noid_hw).all()
        current_user = request.user.get_username()
        context_dict = {
            'tindakan_list':tindakan_list,
            'current_user':current_user,
            'noid_tin':noid_tin,
            'noid_hw':noid_hw,
            'merek':merek,
            'tipe':tipe,
            'lokasi':lokasi,
            'username':username,
            'tanggal_buka':tanggal_buka,
            'tanggal_tutup':tanggal_tutup,
            'first_name':first_name,
            'jenis_tindakan':jenis_tindakan,
            'masalah':masalah,
            'penyelesaian':penyelesaian,
            'kathw':kathw,
            'status':status,
            'status_proses':status_proses,
            'status_tunda':status_tunda,
            'status_batal':status_batal,
            'status_selesai':status_selesai,

            }
        return render_to_response('main/tindakan_detail.html', context_dict, context)
        # return HttpResponse('hello')

    else :
        return HttpResponseRedirect("/main/login")

def perangkat_update(request):
    if request.user.is_authenticated():
        context = RequestContext(request)
        if request.method == 'POST':
            noid_hw = request.POST['noid_hw']
            kodebrg = request.POST['kodebrg']
            merek = request.POST['merek']
            tipe = request.POST['tipe']
            lokasi = request.POST['lokasi']
            tahun = request.POST['tahun']
            kathw = request.POST['kathw']
            username = request.POST['username']
            keterangan = request.POST['keterangan']
            if tahun=='':
                tahun='0000'
            if kodebrg=='':
                kodebrg='0000'
            from main.models import Hardware, User, Tindakan, Lokasi, Kathw
            lokasi=Lokasi.objects.get(lokasi=lokasi)
            kathw=Kathw.objects.get(kathw=kathw)
            username=User.objects.get(username=username)
            perangkat = Hardware.objects.filter(noid_hw=noid_hw).get()
            perangkat.kodebrg=kodebrg
            perangkat.merek=merek
            perangkat.tipe=tipe
            perangkat.lokasi=lokasi
            perangkat.kathw=kathw
            perangkat.username=username
            perangkat.tahun=tahun
            perangkat.keterangan=keterangan
            perangkat.save()
            # return HttpResponse(p)
            return HttpResponseRedirect("/main/perangkat/")
        else:
            return HttpResponseRedirect("/main/perangkat/")
    else :
        return HttpResponseRedirect("/main/login")

def perangkat(request):
    if request.user.is_authenticated():
        context = RequestContext(request)
        if request.method == 'POST':
            kodebrg = request.POST['kodebrg']
            merek = request.POST['merek']
            tipe = request.POST['tipe']
            lokasi = request.POST['lokasi']
            tahun = request.POST['tahun']
            kathw = request.POST['kathw']
            username = request.POST['username']
            keterangan = request.POST['keterangan']
            if tahun=='':
                tahun='0000'
            if kodebrg=='':
                kodebrg='0000'
            from main.models import Hardware, User, Tindakan, Lokasi, Kathw
            lokasi=Lokasi.objects.get(lokasi=lokasi)
            kathw=Kathw.objects.get(kathw=kathw)
            username=User.objects.get(username=username)

            import time
            time_create = time.time()

            Hardware.objects.get_or_create(kodebrg=kodebrg,merek=merek,tipe=tipe,lokasi=lokasi, kathw=kathw, username=username, tahun=tahun, keterangan=keterangan, time_create=time_create)
            # return HttpResponse(p)
            return HttpResponseRedirect("/main/perangkat/")
        else:
            context = RequestContext(request)
            from main.models import Hardware, User, Tindakan, Lokasi, Kathw


            if bool(request.GET):
                # filter = request.GET['filter']
                kathw = request.GET['kathw']
                lokasi = request.GET['lokasi']
                perangkat_list = Hardware.objects.filter(kathw=kathw).filter(lokasi=lokasi).order_by('kathw')
                if kathw=='Semua':
                    perangkat_list = Hardware.objects.filter(lokasi=lokasi).order_by('kathw')
                if lokasi=='Semua':
                    perangkat_list = Hardware.objects.filter(kathw=kathw).order_by('kathw')
                if kathw=='Semua' and lokasi=='Semua':
                    perangkat_list = Hardware.objects.order_by('kathw')

                kathw_list = Kathw.objects.all()
                lokasi_list = Lokasi.objects.all()
                user_list = User.objects.all()

                banyak = len(perangkat_list)
                current_user = request.user.get_username()
                context_dict = {'perangkat_list':perangkat_list,'kathw_list':kathw_list, 'lokasi_list':lokasi_list,'user_list':user_list,'current_user':current_user,'lokasi':lokasi,'kathw':kathw, 'banyak':banyak}
                return render_to_response('main/perangkat.html', context_dict, context)

            else:
                perangkat_list = Hardware.objects.all().order_by('kathw')
                kathw_list = Kathw.objects.all()
                lokasi_list = Lokasi.objects.all()
                user_list = User.objects.all()
                current_user = request.user.get_username()
                lokasi='Semua'
                kathw='Semua'
                banyak = len(perangkat_list)
                context_dict = {'perangkat_list':perangkat_list,'kathw_list':kathw_list, 'lokasi_list':lokasi_list,'user_list':user_list,'current_user':current_user,'lokasi':lokasi,'kathw':kathw, 'banyak':banyak}
                return render_to_response('main/perangkat.html', context_dict, context)
    else :
        return HttpResponseRedirect("/main/login")


def closed(request):

    if request.user.is_authenticated():
        return HttpResponse('halaman ini tertutup, harus login untuk melihat, anda dapat melihatnya karena anda sudah login')
    else :
        return HttpResponse('Anda belum login.')

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('../../main/')
            else:
                return HttpResponse('Your account is disabled')
        else:
            # print "Invalid login details : {0}, {1}".format.(username, password)
            return HttpResponseRedirect('../../main/login/?result=fail')
    else:
        if bool(request.GET):
            if request.GET['result']=='fail':
                context_dict={'result':'Nama akun atau password anda salah.'}
                return render_to_response('main/login.html', context_dict, context)
                # return HttpResponse('arst')
            pass
        return render_to_response('main/login.html', {}, context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/main/')
