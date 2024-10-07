from django.core.management.base import BaseCommand

from parsers.parser_flamp import ParserFlamp

class Command(BaseCommand):
	help = "Тест парсера"

	def handle(self, *args, **options):
		parser = ParserFlamp("https://moscow.flamp.ru/firm/gorynych_restoran-70000001031017075")

		parser.parse_rating()
		parser.parse_reviews()
		parser.close_page()

