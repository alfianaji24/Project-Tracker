from django.core.management.base import BaseCommand

from core.models import ContractType, ProjectStatus, ProjectType, TOP


class Command(BaseCommand):
    help = "Seed master data sesuai PRD (Contract Type, Project Type, TOP, Project Status)."

    def handle(self, *args, **options):
        contract_types = [
            ("PKSS", "PKS"),
            ("POSP", "PO"),
        ]
        project_types = [
            ("CLDY", "Cloud"),
            ("ITAS", "ITaaS"),
            ("PROJ", "Project"),
        ]
        tops = [
            ("MNTH", "Monthly", ""),
            ("ANUL", "Annual", ""),
            ("OTIM", "1 Times", ""),
            ("PROG", "Progress", ""),
        ]
        project_statuses = [
            ("DRAF", "Draft"),
            ("ONGO", "On Going"),
            ("DONE", "Completed"),
            ("EXPR", "Expired"),
            ("CANC", "Cancelled"),
        ]

        for code, name in contract_types:
            ContractType.objects.update_or_create(code=code, defaults={"name": name})

        for code, name in project_types:
            ProjectType.objects.update_or_create(code=code, defaults={"name": name})

        for code, name, description in tops:
            TOP.objects.update_or_create(
                code=code,
                defaults={"name": name, "description": description},
            )

        for code, name in project_statuses:
            ProjectStatus.objects.update_or_create(code=code, defaults={"name": name})

        self.stdout.write(self.style.SUCCESS("Master data seeded successfully."))
