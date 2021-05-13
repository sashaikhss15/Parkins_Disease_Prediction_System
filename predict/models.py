from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from multiselectfield import MultiSelectField

from data.models import DiseaseModel

class PredictModel(models.Model):
    Symptoms = [
        ('itching', 'Itching'),
        ('skin_rash', 'Skin Rash'),
        ('nodal_skin_eruptions', 'Nodal Skin Eruptions'),
        ('continuous_sneezing', 'Continuous Sneezing'),
        ('shivering', 'Shivering'),
        ('chills', 'Chills'),
        ('joint_pain', 'Joint Pain'),
        ('stomach_pain', 'Stomach Pain'),
        ('acidity', 'Acidity'),
        ('ulcers_on_tongue', 'Uclers On Tongue'),
        ('muscle_wasting', 'muscle_wasting'),
        ('vomiting', 'Vomiting'),
        ('burning_micturition', 'Burning Micturition'),
        ('spotting_urination', 'Spotting Urination'),
        ('fatigue', 'Fatigue'),
        ('weight_gain', 'Weight Gain'),
        ('anxiety', 'Anxiety'),
        ('cold_hands_and_feets', 'Cold Hands And Feets'),
        ('mood_swings', 'Mood Swings'),
        ('weight_loss', 'Weight Loss'),
        ('restlessness', 'Relentlessness'),
        ('lethargy', 'Lethargy'),
        ('patches_in_throat', 'Patches In Throat'),
        ('irregular_sugar_level', 'Irregular Sugar Level'),
        ('cough', 'Cough'),
        ('high_fever', 'High Fever'),
        ('sunken_eyes', 'Sunken Eyes'),
        ('breathlessness', 'Breathlessness'),
        ('sweating', 'Sweating'),
        ('dehydration', 'Dehydration'),
        ('indigestion', 'Indigestion'),
        ('headache', 'Headache'),
        ('yellowish_skin', 'Yellowish Skin'),
        ('dark_urine', 'Dark Urine'),
        ('nausea', 'Nausea'),
        ('loss_of_appetite', 'Loss of Appetite'),
        ('pain_behind_the_eyes', 'Pain Behind the Eyes'),
        ('back_pain', 'Back Pain'),
        ('constipation', 'Constipation'),
        ('abdominal_pain', 'Abdominal Pain'),
        ('diarrhoea', 'Diarrhoea'),
        ('mild_fever', 'Mild Fever'),
        ('yellow_urine', 'Yellow Urine'),
        ('yellowing_of_eyes', 'Yellowing of Eyes'),
        ('acute_liver_failure', 'Actuate Liver Failure'),
        ('fluid_overload', 'Fluid Overload'),
        ('swelling_of_stomach', 'Swelling of Stomach'),
        ('swelled_lymph_nodes', 'Swelled Lymph Nodes'),
        ('malaise', 'Malaise'),
        ('blurred_and_distorted_vision', 'Blurred and Distorted Vision'),
        ('phlegm', 'Phlegm'),
        ('throat_irritation', 'Throat Irritation'),
        ('redness_of_eyes', 'Redness of Eyes'),
        ('sinus_pressure', 'Sinus Pressure'),
        ('runny_nose', 'Runny Nose'),
        ('congestion', 'Congestion'),
        ('chest_pain', 'Chest Pain'),
        ('weakness_in_limbs', 'Weakness in Limbs'),
        ('fast_heart_rate', 'Fast Heart Rate'),
        ('pain_during_bowel_movements', 'Pain during Bowel Movements'),
        ('pain_in_anal_region', 'Pain in Anal Region'),
        ('bloody_stool', 'Bloody Stool'),
        ('irritation_in_anus', 'Irritation in Anus'),
        ('neck_pain', 'Neck Pain'),
        ('dizziness', 'Dizziness'),
        ('cramps', 'Cramps'),
        ('bruising', 'Bruising'),
        ('obesity', 'Obesity'),
        ('swollen_legs', 'Swollen Legs'),
        ('swollen_blood_vessels', 'Swollen Blood Vessels'),
        ('puffy_face_and_eyes', 'Puffy Face and Eyes'),
        ('enlarged_thyroid', 'Enlarged Thyroid'),
        ('brittle_nails', 'Brittle Nails'),
        ('swollen_extremeties', 'Swollen Extremeties'),
        ('excessive_hunger', 'Excessive Hunger'),
        ('extra_marital_contacts', 'Extra Marital Contacts'),
        ('drying_and_tingling_lips', 'Drying and Tingling Lips'),
        ('slurred_speech', 'Slurred Speech'),
        ('knee_pain', 'Knee Pain'),
        ('hip_joint_pain', 'Hip Joint Pain'),
        ('muscle_weakness', 'Muscle Weakness'),
        ('stiff_neck', 'Stiff Neck'),
        ('swelling_joints', 'Swelling Joints'),
        ('movement_stiffness', 'Movement Stiffness'),
        ('spinning_movements', 'Spinning Movements'),
        ('loss_of_balance', 'Loss of Balance'),
        ('unsteadiness', 'Unsteadiness'),
        ('weakness_of_one_body_side', 'Weakness of One Body Side'),
        ('loss_of_smell', 'Loss of Smell'),
        ('bladder_discomfort', 'Bladder Discomfort'),
        ('foul_smell_of_urine', 'Foul Smell of Urine'),
        ('continuous_feel_of_urine', 'Continuous Feel of Urine'),
        ('passage_of_gases', 'Passage of Gases'),
        ('internal_itching', 'Internal Itching'),
        ('toxic_look_(typhos)', 'Toxic Look (Typhos)'),
        ('depression', 'Depression'),
        ('irritability', 'Irritability'),
        ('muscle_pain', 'Muscle Pain'),
        ('altered_sensorium', 'Altered Sensorium'),
        ('red_spots_over_body', 'Red Spots Over Body'),
        ('belly_pain', 'Belly Pain'),
        ('abnormal_menstruation', 'Abnormal Menstruation'),
        ('dischromic_patches', 'Dischromic Patches'),
        ('watering_from_eyes', 'Watering from Eyes'),
        ('increased_appetite', 'Increased Appetite'),
        ('polyuria', 'Polyuria'),
        ('family_history', 'Family History'),
        ('mucoid_sputum', 'Mucoid Sputum'),
        ('rusty_sputum', 'Rusty Sputum'),
        ('lack_of_concentration', 'Lack of Concentration'),
        ('visual_disturbances', 'Visual Disturbances'),
        ('receiving_blood_transfusion', 'Receiving Blood Transfusion'),
        ('receiving_unsterile_injections', 'Receiving Un-sterile Injections'),
        ('coma', 'Coma'),
        ('stomach_bleeding', 'Stomach Bleeding'),
        ('distention_of_abdomen', 'Distention of Abdomen'),
        ('history_of_alcohol_consumption', 'History of Alcohol Consumption'),
        ('fluid_overload', 'Fluid Overload'),
        ('blood_in_sputum', 'Blood in Sputum'),
        ('prominent_veins_on_calf', 'Prominent Veins on Calf'),
        ('palpitations', 'Palpitations'),
        ('painful_walking', 'Painful Walking'),
        ('pus_filled_pimples', 'Pus filled Pimples'),
        ('blackheads', 'Blackheads'),
        ('scurring', 'Scurring'),
        ('skin_peeling', 'Skin Peeling'),
        ('silver_like_dusting', 'Silver like Dusting'),
        ('small_dents_in_nails', 'Small Dents in Nails'),
        ('inflammatory_nails', 'Inflammatory Nails'),
        ('blister', 'Blister'),
        ('red_sore_around_nose', 'Red Sore around Nose'),
        ('yellow_crust_ooze', 'Yellow Crust Ooze'),
    ]

    Symptoms.sort(key=lambda x: x[0])

    patient_username = models.CharField(max_length=100, default='anonymous')
    patient_name = models.CharField(max_length=100, default='Anonymous')
    symptoms = MultiSelectField(choices=Symptoms, default=Symptoms[0])

    def __str__(self):
        return f'{self.patient_name} - {self.patient_username} - {self.symptoms}'


class PredictedDiseaseModel(models.Model):
    predict_model = models.ForeignKey(PredictModel, on_delete=models.CASCADE)
    disease_name = models.CharField(max_length=100)
    prediction_confidence = models.DecimalField(
        validators=(MinValueValidator(Decimal(00.00)), MaxValueValidator(Decimal(100.00))),
        max_digits=5, decimal_places=2, max_length=5, default=00.00)
    is_approved = models.BooleanField(default=False)
    approved_by = models.CharField(max_length=100, default='', blank=True, null=True)
    rejected_by = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return f'{self.predict_model} - {self.disease_name} - {self.prediction_confidence}'


class MyPredictModel(models.Model):
    parameters = models.ForeignKey(DiseaseModel, on_delete=models.CASCADE, null=True, blank=True)
    # is_parkinson

#
# class ParkinResultModel(models.Model):
#     # DiseaseModel
#     # is_parkinson

