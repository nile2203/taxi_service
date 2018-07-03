from django.db import transaction
from ola.models import DriverDocument, UserAccount


class DriverDocuments:
    def __init__(self, type=None, driver=None):
        self.document_type = type
        self.driver = driver

    def upload_driver_documents(self, documents):
        # function which uploads the document to cloud
        try:
            with transaction.atomic():
                DriverDocuments.upload_license(documents[0])
                DriverDocuments.upload_permit(documents[1])
                DriverDocuments.upload_pan(documents[2])
                DriverDocuments.upload_rc(documents[3])
                DriverDocuments.upload_insurance(documents[4])
                self.driver.profile_status = UserAccount.STATUS_PROCESSING
                self.driver.save()

        except Exception as e:
            return 0, "Upload not successfull"
        return 1, "Documents uploaded successfully"

    @staticmethod
    def upload_license(document):
        licence = DriverDocument.objects.create(docuemnt_type=DriverDocument.DRIVING_LICENCE, description="Drivers licence")
        document_url = DriverDocuments.upload_document(document)
        licence.document_url = document_url
        licence.save()

    @staticmethod
    def upload_permit(document):
        permit = DriverDocument.objects.create(docuemnt_type=DriverDocument.VEHICLE_PERMIT, description="Vehicle Permit")
        document_url = DriverDocuments.upload_document(document)
        permit.document_url = document_url
        permit.save()

    @staticmethod
    def upload_pan(document):
        pan = DriverDocument.objects.create(docuemnt_type=DriverDocument.PAN_CARD, description="Pan card")
        document_url = DriverDocuments.upload_document(document)
        pan.document_url = document_url
        pan.save()

    @staticmethod
    def upload_rc(document):
        rc = DriverDocument.objects.create(docuemnt_type=DriverDocument.VEHICLE_RC, description="Vehicle RC")
        document_url = DriverDocuments.upload_document(document)
        rc.document_url = document_url
        rc.save()

    @staticmethod
    def upload_insurance(document):
        insurance = DriverDocument.objects.create(docuemnt_type=DriverDocument.VEHICLE_INSURANCE, description="Vehicle Insurance")
        document_url = DriverDocuments.upload_document(document)
        insurance.document_url = document_url
        insurance.save()

    def upload_bank_proof(self, document):
        proof = DriverDocument.objects.create(docuemnt_type=self.document_type, description=self.document_type.lower())
        document_url = DriverDocuments.upload_document(document)
        proof.document_url = document_url
        proof.save()

    @staticmethod
    def upload_document(document):
        return True
