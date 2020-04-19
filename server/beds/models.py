"""
Copyright (c) 2020 Magic LEMP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from django.db import models
from django.utils import timezone
from django.utils.datetime_safe import date

from django.db.models.deletion import CASCADE, PROTECT, SET_NULL


class ReanimationService(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    hospital = models.ForeignKey("users.Hospital", on_delete=CASCADE, blank=False, null=False)
    access_code = models.CharField(max_length=10, blank=False, null=False)

    @property
    def units(self):
        return get_units(self).all()

    class Meta:
        unique_together = [["name", "hospital"]]

    def __str__(self):
        return f"Réanimation {self.name} - {self.hospital}"


def get_units(rea: ReanimationService):
    units = Unit.objects.filter(reanimation_service=rea.id)
    return units


class Unit(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    reanimation_service = models.ForeignKey(ReanimationService, on_delete=PROTECT, blank=False, null=False)

    @property
    def beds(self):
        return get_beds(self).all()

    class Meta:
        unique_together = [["name", "reanimation_service"]]

    def __str__(self):
        return f"Unité {self.name} ({self.reanimation_service})"


def get_beds(unit: Unit):
    beds = Bed.objects.filter(unit=unit.id)
    return beds


class Bed(models.Model):
    unit = models.ForeignKey(Unit, related_name='beds', on_delete=CASCADE, blank=False, null=False)
    # quel numéro ce lit porte dans l'unité
    unit_index = models.IntegerField(blank=False, null=False)
    status = models.IntegerField(choices=[(0, "Utilisable"), (1, "Inutilisable")], default="usable")

    @property
    def current_stay(self):
        return get_current_unit_stay(self).first()

    @property
    def is_unusable(self):
        return self.status == 1

    class Meta:
        unique_together = [["unit", "unit_index"]]

    def __str__(self):
        return f"{self.id} - Lit {self.unit_index} - {self.unit} " \
               f"{'(' + self.current_stay.patient.NIP_id + ')' if self.current_stay else ''}"


def get_current_unit_stay(bed: Bed):
    stays = UnitStay.objects.filter(bed=bed.id)
    today = date.today()
    stays = stays.filter(start_date__lte=today).filter(end_date=None)
    return stays


def get_reanimation_service_from_bed(bed_id: Bed):
    bed = Bed.objects.filter(id=bed_id).first()
    if bed is None:
        return None
    unit = Unit.objects.get(id=bed.unit)
    rea = ReanimationService.objects.filter(id=unit.reanimation_service).first()
    return rea


class UnitStay(models.Model):
    created_by = models.ForeignKey("users.UserProfile", related_name='unit_stays_created', on_delete=SET_NULL, blank=True, null=True)
    patient = models.ForeignKey("patients.Patient", related_name='beds', on_delete=CASCADE, blank=False, null=False)
    bed = models.ForeignKey(Bed, related_name='stays', on_delete=PROTECT, blank=False, null=False)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        date_format = '%d-%m-%Y'
        if self.is_finished:
            date_info = 'entre le ' + self.start_date.strftime(date_format) \
                        + ' et le ' + self.end_date.strftime(date_format)
        else:
            date_info = 'depuis le ' + self.start_date.strftime(date_format)
        return f"{self.id} - Patient {str(self.patient)}, {str(self.bed.unit)} ({date_info})"

    @property
    def is_finished(self):
        return self.end_date is not None

    @property
    def bed_description(self):
        return str(self.bed)
