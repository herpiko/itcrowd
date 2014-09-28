from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Lokasi(models.Model):
	lokasi = models.CharField(max_length=50,primary_key=True)

class Kathw(models.Model):
	kathw = models.CharField(max_length=20,primary_key=True)

class Hardware(models.Model):
	noid_hw = models.AutoField(primary_key=True)
	kodebrg = models.CharField(max_length=50)
	merek = models.CharField(max_length=50)
	tipe = models.CharField(max_length=50)
	kathw = models.ForeignKey(Kathw)
	username = models.ForeignKey(User)
	lokasi = models.ForeignKey(Lokasi)
	tahun = models.IntegerField()
	keterangan = models.CharField(max_length=500)
	time_create = models.CharField(max_length=50)
	

class Tindakan(models.Model):
	noid_tin = models.AutoField(primary_key=True)
	noid_hw = models.ForeignKey(Hardware)
	username = models.ForeignKey(User)
	tanggal_buka = models.CharField(max_length=50)
	tanggal_tutup = models.CharField(max_length=50)
	jenis_tindakan = models.CharField(max_length=500)
	masalah = models.CharField(max_length=500)
	penyelesaian = models.CharField(max_length=500)
	status = models.CharField(max_length=20)
	time_create = models.CharField(max_length=50)

class Perubahan(models.Model):
	noid_hw = models.ForeignKey(Hardware)
	perubahan = models.CharField(max_length=200)



