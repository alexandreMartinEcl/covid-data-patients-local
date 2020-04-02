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
import hashlib
import django.db.models.fields as fields
from django.utils.translation import gettext_lazy as _
# from protected_media.models import ProtectedImageField


def get_field_schema(field, title):
    """Returns a JSON Schema representation of a form field."""
    field_schema = {
        'type': 'string',
        'title': title
    }

    # field_schema['title'] = str(field.label)  # force translation

    # if field.help_text:
    #     field_schema['description'] = str(field.help_text)  # force translation

    # if isinstance(field, (fields.URLField, fields.FileField)):
    #     field_schema['format'] = 'uri'
    # elif isinstance(field, fields.EmailField):
    #     field_schema['format'] = 'email'
    if isinstance(field, fields.DateTimeField):
        field_schema['format'] = 'date-time'
    elif isinstance(field, fields.DateField):
        field_schema['format'] = 'date'
    # elif isinstance(field, ProtectedImageField):
    #     field_schema['format'] = 'data-url'
    elif isinstance(field, (fields.DecimalField, fields.FloatField)):
        field_schema['type'] = 'number'
    elif isinstance(field, fields.IntegerField):
        field_schema['type'] = 'integer'
        if getattr(field, 'hidden_boolean', []):
            if field.hidden_boolean:
                field_schema['type'] = 'boolean'
    elif isinstance(field, (fields.NullBooleanField, fields.BooleanField)):
        field_schema['type'] = 'boolean'
        field_schema['default'] = False
    # elif isinstance(field.widget, widgets.CheckboxInput):
    #     field_schema['type'] = 'boolean'

    if getattr(field, 'choices', []) and not isinstance(field, (fields.NullBooleanField, fields.BooleanField)):
        field_schema['enum'] = sorted([choice[0] for choice in field.choices])
        # print(field.default)
        # print(type(field.default))
        if type(field.default) is int:
            field_schema['default'] = field.default

    if getattr(field, 'minmax', []):
        field_schema['python_minimum'] = field.minmax[0]
        field_schema['python_maximum'] = field.minmax[1]

    # check for multiple values

    return field_schema


class Patient(models.Model):
    # id_key = models.CharField(blank=False, null=False)
    inclusion_nb = models.CharField(max_length=200)
    inclusion_code = models.CharField(max_length=200)
    hospital = models.ForeignKey('users.Hospital', on_delete=models.PROTECT)
    age = models.IntegerField()  # in years
    age.minmax = (0, 120)

    size = models.FloatField()  # in m
    size.minmax = (0, 300)

    weight = models.FloatField()  # in kg
    weight.minmax = (0, 150)

    duree_symptomes = models.IntegerField()

    # image_test = ProtectedImageField(upload_to="uploads/", blank=True)

    cardio_past = models.IntegerField(
        choices=[
            (0, "no previous condition"),
            (1, "minor condition: heart murmur"),
            (2, "major condition: IDM, cardiac failure")
        ], default=0)
    pneumo_past = models.IntegerField(
        choices=[
            (0, "no previous condition"),
            (1, "asthma")
        ], default=0)
    chir_past = models.IntegerField(
        choices=[
            (0, "no former surgery"),
            (1, "torax_surgery"),
            (2, "abdominal surgery"),
            (3, "orthopedic surgery"),
            (4, "torax + abdominal"),
            (5, "torax + abdominal + orthopedic "),
            (6, "abdominal + orthopedic")
        ], default=0)
    # Symptoms
    data_diagnostic = models.DateField()
    data_hospital = models.DateField()
    data_reanimation = models.DateField(blank=True)

    # booleans
    cough = models.BooleanField()
    fever = models.BooleanField()
    appetite_loss = models.BooleanField()
    dispnea = models.BooleanField()
    sore_throat = models.BooleanField()
    diarrhea = models.BooleanField()
    nausea = models.BooleanField()
    vertigo = models.BooleanField()
    headache = models.BooleanField()
    vomit = models.BooleanField()

    score_sofa = models.IntegerField()
    score_sofa.minmax = (0, 15)

    # Situation
    so2_admission = models.FloatField()
    so2_admission.minmax = (50, 100)

    ta_systolic_admission = models.FloatField()
    ta_systolic_admission.minmax = (80, 220)

    ta_diastolic_admission = models.FloatField()
    ta_diastolic_admission.minmax = (50, 150)

    hospitalization_type = models.IntegerField(
        choices=[
            (0, "ambulatory"),
            (1, "conventional"),
            (2, "intensive care"),
            (3, "reanimation"),
            (4, "reanimation + ECMO")
        ])

    # TDM admission
    tdm_ad_frosted_glass = models.BooleanField()
    tdm_ad_atelectasie = models.BooleanField()
    tdm_ad_pleural_obstruction = models.BooleanField()

    # nouvelles features
    surinfection_bacterienne = models.BooleanField()

    traitement_en_cours = models.IntegerField(choices=[
        (0, "Pas de traitement"),
        (1, "Antibiothérapie")
    ])

    @staticmethod
    def hash(code_or_nb: str):
        # return hashlib.sha1(code_or_nb.encode("UTF-*"))
        return code_or_nb

    @classmethod
    def get_react_description(cls):
        required = []

        json_schema = {
            "title": _("Informations générales du patient"),
            "description": _("Informations générales du patient"),
            "type": "object",
            "required": required,
            "properties": {
            }
        }

        all_fields = cls._meta.fields

        translations = {}
        for field in all_fields:
            translations[field.name] = field.name

        top_cluster = [
            "id"
        ]

        cluster_general = [
            "inclusion_nb",
            "inclusion_code",
            "age",
            "size",
            "weight",
            "data_diagnostic",
            "data_hospital",
            "data_reanimation",
            "hospitalization_type"
        ]

        cluster_bio = [
            "cardio_past",
            "pneumo_past",
            "chir_past",
            "cough",
            "fever",
            "appetite_loss",
            "dispnea",
            "sore_throat",
            "diarrhea",
            "nausea",
            "vertigo",
            "headache",
            "vomit",
            "so2_admission",
            "ta_systolic_admission",
            "ta_diastolic_admission",
            "tdm_ad_frosted_glass",
            "tdm_ad_atelectasie",
            "tdm_ad_pleural_obstruction",
            "surinfection_bacterienne",
            "traitement_en_cours",
            "duree_symptomes",
            # "image_test",
            "score_sofa"
        ]

        cluster_all = cluster_general + cluster_bio

        translations["inclusion_nb"] = _("Numéro d'inclusion")
        translations["inclusion_code"] = _("Code centre inclusion")
        translations["age"] = _("Age")
        translations["size"] = _("Taille")
        translations["weight"] = _("Poids")

        translations["cardio_past"] = _("Antécédants cardiovasculaires")
        translations["pneumo_past"] = _("Antécédants pneumos")
        translations["chir_past"] = _("Antécédants chirurgicaux")

        translations["data_diagnostic"] = _("Date de diagnostic positif")
        translations["data_hospital"] = _("Date d'admission en hospitalisation")
        translations["data_reanimation"] = _("Date d'admission en soins intensifs réanimation")

        translations["cough"] = _("Toux")
        translations["fever"] = _("Fièvre (> 37.8 C)")
        translations["appetite_loss"] = _("Perte d'apétit")
        translations["dispnea"] = _("Dyspnée")
        translations["sore_throat"] = _("Maux de gorge")
        translations["diarrhea"] = _("Diarrhée")
        translations["nausea"] = _("Nausée")
        translations["vertigo"] = _("Vertiges")
        translations["headache"] = _("Céphalées")
        translations["vomit"] = _("Vomissments")

        translations["so2_admission"] = _("Saturation 02 à l'admission")
        translations["ta_systolic_admission"] = _("TA systolique à l'admission")
        translations["ta_diastolic_admission"] = _("TA diastolique à l'admission")

        translations["hospitalization_type"] = _("Type d'hospitalisation")

        translations["tdm_ad_frosted_glass"] = _("Verre dépoli")
        translations["tdm_ad_atelectasie"] = _("Atelectasie")
        translations["tdm_ad_pleural_obstruction"] = _("Epenchement pleural")
        translations["surinfection_bacterienne"] = _("Surinfection bactérienne")
        translations["traitement_en_cours"] = _("Traitement en cours")
        translations["duree_symptomes"] = _("Durée des symptomes")

        translations["score_sofa"] = _("Score SOFA")

        local_json_schemas = {}
        for field in all_fields:
            if field.name in ['hospital']:
                continue
            local_json_schema = get_field_schema(field, translations[field.name])
            local_json_schemas[field.name] = local_json_schema
            if not field.blank and type(field) is not fields.BooleanField:
                required.append(field.name)
        
        local_json_schemas['cardio_past']['enumNames'] = [
            _("Pas d'antécédant"),
            _("Antécédant mineur : souffle cardiaque"),
            _("Antécédant")
        ]

        local_json_schemas['pneumo_past']['enumNames'] = [
            _("Pas d'antécédant"),
            _("Athme / BPCO")
        ]

        local_json_schemas['chir_past']['enumNames'] = [
            _("Pas d'antécédant"),
            _("Chirurgie thoracique"),
            _("Chirurgie abdominale"),
            _("Chirurgie orthopédique"),
            _("Chirurgie thoracique + abdominale"),
            _("Chirurgie thorcique + abdominale + orthopédique"),
            _("Chirurgie abdominale + orthopédique")
        ]

        local_json_schemas["hospitalization_type"]["enumNames"] = [
            _("ambulatoire"),
            _("conventionel"),
            _("soin intensif"),
            _("reanimation"),
            _("reanimation + ECMO")
        ]

        local_json_schemas['traitement_en_cours']["enumNames"] = [
            _("Pas de traitement"),
            _("Antibiothérapie")
        ]

        def cluster_to_properties(cluster):
            res = {}
            for name in cluster:
                res[name] = local_json_schemas[name]
            return res

        json_schema['properties'] = {
            'general': {
                'title': _('Données génerales'),
                'type': 'object',
                'properties': cluster_to_properties(cluster_general)
            },
            'bio': {
                'title': _('Données biologiques'),
                'type': 'object',
                'properties': cluster_to_properties(cluster_bio)
            },
        }

        for field_name in top_cluster:
            json_schema['properties'][field_name] = local_json_schemas[field_name]

        return json_schema


class Ventilation(models.Model):

    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    day = models.DateTimeField(auto_now_add=True)

    volume = models.FloatField()  # in mL/kg

    respiratory_freq = models.FloatField()
    respiratory_freq.minmax = (0, 80)

    plateau_pressure_30cm2 = models.FloatField()
    plateau_pressure_30cm2 = (0, 50)

    """
    teleinspiratory_ventilatory_pause = models.IntegerField()
    teleinspiratory_ventilatory_pause.hidden_boolean = True
    """
    teleinspiratory_ventilatory_pause = models.BooleanField()

    tv_pause_duration = models.FloatField()

    positive_expiratory_pressure = models.FloatField()
    positive_expiratory_pressure.minmax = (0, 15)

    """
    ventral_decubitis = models.IntegerField()
    ventral_decubitis.hidden_boolean = True
    """
    ventral_decubitis = models.BooleanField()

    curare = models.FloatField(default=0)
    NO = models.FloatField(default=0)

    clinical_situation = models.IntegerField(
        choices=[
            (0, "stable"),
            (1, "improvement"),
            (2, "degradation"),
            (4, "death"),
            (5, "extubation")
        ])

    # Nouvelle features
    pa = models.FloatField()

    temperature = models.FloatField()
    temperature.minmax = (34, 45)

    saturation_o2 = models.FloatField()
    saturation_o2.minmax = (50, 100)

    score_respiration_pao2_fio2 = models.FloatField()
    score_respiration_pao2_fio2.minmax = (0, 500)

    ventilation_artificielle = models.BooleanField()

    score_coagulation = models.FloatField()
    score_coagulation.minmax = (0, 200)

    score_hepatique = models.FloatField()
    score_hepatique.minmax = (0, 250)

    score_cardiovasculaire = models.IntegerField(choices=[
        (0, "Absence d'hypotension"),
        (1, "PAmoy < 70 mmHg  sans drogue vasoactive"),
        (2, "Utilisation Dopamine (< 5µg/kg/mn) ou Dobutamine"),
        (3, "Utilisation Dopamine (> 5µg/kg/mn) ou Noradrénaline/Adrénaline (< 0.1 µg/kg/mn)"),
        (4, "Utilisation Dopamine (> 15 µg/kg/mn) ou Noradrénaline/Adrénaline (> 0.1 µg/kg/mn)")
    ])

    score_sofa = models.IntegerField()
    score_sofa.minmax = (0, 15)

    score_neurologique = models.IntegerField()
    score_neurologique.minmax = (0, 15)

    score_renal_creatine = models.FloatField()
    score_renal_creatine.minmax = (0, 500)

    score_renal_diurese = models.FloatField()
    score_renal_diurese.minmax = (0, 1000)

    @classmethod
    def get_react_description(cls):
        required = []
        json_schema = {
            "title": _("Informations générales du patient"),
            "description": _("Informations générales du patient"),
            "type": "object",
            "required": required,
            "properties": {
            }
        }

        all_fields = cls._meta.fields

        translations = {}
        for field in all_fields:
            translations[field.name] = field.name

        translations["patient"] = _("Patient")
        translations["day"] = _("Date")
        translations["volume"] = _("Volume (mL/kg)")
        translations["respiratory_freq"] = _("Fréquence respiratoire")
        translations["plateau_pressure_30cm2"] = _("Pression de plateau 30cm2")
        translations["teleinspiratory_ventilatory_pause"] = _("Pause ventilatoire téléinspiratoire")
        translations["tv_pause_duration"] = _("Durée pause téléinspiratoire")
        translations["positive_expiratory_pressure"] = _("Pression expiratoire positive")
        translations["ventral_decubitis"] = _("Positionnement en décubitis ventral")
        translations["curare"] = _("Curare")
        translations["NO"] = _("NO")
        translations["clinical_situation"] = _("Évolution clinique")
        # Nouvelle features
        translations["pa"] = _("PA")
        translations["temperature"] = _("Temperature")
        translations["saturation_o2"] = _("Saturation O2")

        translations["score_respiration_pao2_fio2"] = _("Respiration PaO2/FiO2")
        translations["score_coagulation"] = _("Coagulation mm3")
        translations["score_hepatique"] = _("Hépatique µmol/L")
        translations["score_cardiovasculaire"] = _("Score cardiovasculaire")
        translations["score_neurologique"] = _("Score de Glasgow")
        translations["score_renal_creatine"] = _("Taux de creatine µmol/L")
        translations["score_renal_diurese"] = _("Diurèse mL/24h")
        translations["ventilation_artificielle"] = _("Ventilation artificielle")

        translations["score_sofa"] = _("Score SOFA")

        for field in all_fields:
            if field.name in []:
                continue
            local_json_schema = get_field_schema(field, translations[field.name])
            json_schema['properties'][field.name] = local_json_schema
            if not field.blank and type(field) is not fields.BooleanField:
                required.append(field.name)
 
        json_schema['properties']['clinical_situation']['enumNames']= [
            _("stable"),
            _("amélioration"),
            _("dégradation"),
            _("décès"),
            _("extubation (sortie de réa)")
        ]

        json_schema['properties']['score_cardiovasculaire']['enumNames'] = [
            _("Absence d'hypotension"),
            _("PAmoy < 70 mmHg  sans drogue vasoactive"),
            _("Utilisation Dopamine (< 5µg/kg/mn) ou Dobutamine"),
            _("Utilisation Dopamine (> 5µg/kg/mn) ou Noradrénaline/Adrénaline (< 0.1 µg/kg/mn)"),
            _("Utilisation Dopamine (> 15 µg/kg/mn) ou Noradrénaline/Adrénaline (> 0.1 µg/kg/mn)")
        ]

        return json_schema

