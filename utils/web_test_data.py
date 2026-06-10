from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from faker import Faker


AUTOMATION_PREFIX = "AUTO_WEB"
fake = Faker()


@dataclass(frozen=True)
class WebTestEntity:
    kind: str
    name: str
    email: str


@dataclass(frozen=True)
class CollegeFormData:
    name: str
    city: str
    state: str
    college_type: str
    naac_grade: str
    total_students: str
    placement_percent: str
    email: str
    password: str
    phone: str
    website: str
    address: str
    subscription: str
    mou_status: str


@dataclass(frozen=True)
class OrganizationFormData:
    name: str
    city: str
    state: str
    industry: str
    company_type: str
    email: str
    password: str
    phone: str
    website: str
    address: str
    subscription: str
    mou_status: str


class WebTestDataFactory:
    """Creates deterministic-looking, unique data for live web automation."""

    def __init__(self, prefix: str = AUTOMATION_PREFIX):
        self.prefix = prefix
        self.run_id = datetime.now(UTC).strftime("%Y%m%d%H%M%S")

    def entity(self, kind: str) -> WebTestEntity:
        normalized_kind = kind.upper().replace(" ", "_")
        suffix = uuid4().hex[:8]
        name = f"{self.prefix}_{normalized_kind}_{self.run_id}_{suffix}"
        email = f"{name.lower()}@mailinator.com"
        return WebTestEntity(kind=normalized_kind, name=name, email=email)

    def college(self) -> CollegeFormData:
        entity = self.entity("college")
        return CollegeFormData(
            name=entity.name,
            city="Hyderabad",
            state="Telangana",
            college_type="Engineering",
            naac_grade="A+",
            total_students=str(fake.random_int(min=100, max=9999)),
            placement_percent=str(fake.random_int(min=40, max=98)),
            email=entity.email,
            password="Auto@12345",
            phone=fake.msisdn()[:10],
            website=f"https://{fake.domain_name()}",
            address=fake.street_address(),
            subscription="Basic",
            mou_status="Active",
        )

    def organization(self) -> OrganizationFormData:
        entity = self.entity("company")
        return OrganizationFormData(
            name=entity.name,
            city="Hyderabad",
            state="Telangana",
            industry="IT",
            company_type="Startup",
            email=entity.email,
            password="Auto@12345",
            phone=fake.msisdn()[:10],
            website=f"https://{fake.domain_name()}",
            address=fake.street_address(),
            subscription="Basic",
            mou_status="Active",
        )
