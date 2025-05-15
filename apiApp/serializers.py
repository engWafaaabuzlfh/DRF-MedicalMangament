from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers
from .models import Patiant, Invoice, Diagnosis

class InvoiceSerializer(ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['total', 'Paid', 'number_of_visits']

class DiagnosisSerializer(ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = ['disease', 'note_1', 'note_2']
class PatiantSerializer(ModelSerializer):
    diagnosis = DiagnosisSerializer()
    invoice = InvoiceSerializer()
    doctor = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Patiant
        fields = '__all__'
    

    def create(self, validated_data):
        diagnosis_data = validated_data.pop('diagnosis')
        invoice_data = validated_data.pop('invoice')
        #user = self.context['doctor'] 
        diagnosis = Diagnosis.objects.create(**diagnosis_data)
        invoice = Invoice.objects.create(**invoice_data)
        patiant = Patiant.objects.create(diagnosis=diagnosis, invoice=invoice, **validated_data)
        return patiant
    
    def update(self, instance, validated_data):
        diagnosis_data = validated_data.pop('diagnosis', None)
        invoice_data = validated_data.pop('invoice', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if diagnosis_data:
            diagnosis = instance.diagnosis
            for attr, value in diagnosis_data.items():
                setattr(diagnosis, attr, value)
            diagnosis.save()
        if invoice_data:
            invoice = instance.invoice
            for attr, value in invoice_data.items():
                setattr(invoice, attr, value)
            invoice.save()

        return instance