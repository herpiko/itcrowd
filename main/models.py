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

class Kanban(models.Model):
    noid_kanban = models.AutoField(primary_key=True)
    noid_tin = models.ForeignKey(Tindakan)
    slot = models.CharField(max_length=10)
    urut = models.CharField(max_length=10)
    owner = models.CharField(max_length=50)
    archived = models.CharField(max_length=1)
    def as_json(self):
        return dict(
            noid_kanban = self.noid_kanban,
            noid_tin = self.noid_tin,
            slot = self.slot,
            urut = self.urut,
            owner = self.owner)
