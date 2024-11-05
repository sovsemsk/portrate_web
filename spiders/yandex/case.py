from resources.models import Company
from spiders.utils import driver


def perform(company_id):
    company = Company.objects.get(pk=company_id)

    driver.get(company.parser_link_yandex)


    driver.quit()