# Generated by Django 5.0.4 on 2024-07-29 18:01

from decimal import Decimal

import django.db.models.deletion
import django_resized.forms
import djmoney.models.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_secret', models.CharField(blank=True, db_index=True, null=True, verbose_name='API ключ')),
                ('is_visible_0', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать с 0 звезд?')),
                ('is_visible_1', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать с 1 звездой?')),
                ('is_visible_2', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать с 2 звездами?')),
                ('is_visible_3', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать с 3 звездами?')),
                ('is_visible_4', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать с 4 звездами?')),
                ('is_visible_5', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать с 5 звездами?')),
                ('is_visible_portrate', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать Портрет?')),
                ('is_visible_yandex', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать Яндекс?')),
                ('is_visible_gis', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать 2Гис?')),
                ('is_visible_google', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать Google?')),
                ('is_visible_avito', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать Авито?')),
                ('is_visible_zoon', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать Zoon?')),
                ('is_visible_flamp', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать Flamp?')),
                ('is_visible_yell', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать Yell?')),
                ('is_visible_prodoctorov', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать Продокторов?')),
                ('is_visible_yandex_services', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать Яндекс услуги?')),
                ('is_visible_otzovik', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать Otzovik?')),
                ('is_visible_irecommend', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать Irecommend?')),
                ('is_visible_tripadvisor', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображать Tripadvisor?')),
                ('is_visible_short', models.BooleanField(blank=True, default=False, null=True, verbose_name='отображать короткие?')),
                ('is_first_parsing_yandex', models.BooleanField(blank=True, default=True, null=True, verbose_name='это первый парсинг Яндекс?')),
                ('is_parser_run_yandex', models.BooleanField(blank=True, default=False, null=True, verbose_name='парсер Яндекс сейчас запущен?')),
                ('parser_link_yandex', models.CharField(blank=True, null=True, verbose_name='ссылка Яндекс')),
                ('parser_last_change_at_yandex', models.DateField(blank=True, null=True, verbose_name='дата последнего изменения Яндекс')),
                ('parser_last_parse_at_yandex', models.DateTimeField(blank=True, null=True, verbose_name='дата и время последней загрузки Яндекс')),
                ('is_first_parsing_gis', models.BooleanField(blank=True, default=True, null=True, verbose_name='это первый парсинг 2Гис?')),
                ('is_parser_run_gis', models.BooleanField(blank=True, default=False, null=True, verbose_name='парсер 2Гис сейчас запущен?')),
                ('parser_link_gis', models.CharField(blank=True, null=True, verbose_name='ссылка 2Гис')),
                ('parser_last_change_at_gis', models.DateField(blank=True, null=True, verbose_name='дата последнего изменения 2Гис')),
                ('parser_last_parse_at_gis', models.DateTimeField(blank=True, null=True, verbose_name='дата и время последней загрузки 2Гис')),
                ('is_first_parsing_google', models.BooleanField(blank=True, default=True, null=True, verbose_name='это первый парсинг Google?')),
                ('is_parser_run_google', models.BooleanField(blank=True, default=False, null=True, verbose_name='парсер Google сейчас запущен?')),
                ('parser_link_google', models.CharField(blank=True, null=True, verbose_name='ссылка Google')),
                ('parser_last_change_at_google', models.DateField(blank=True, null=True, verbose_name='дата последнего изменения Google')),
                ('parser_last_parse_at_google', models.DateTimeField(blank=True, null=True, verbose_name='дата и время последней загрузки Google')),
                ('is_first_parsing_avito', models.BooleanField(blank=True, default=True, null=True, verbose_name='это первый парсинг Авито?')),
                ('is_parser_run_avito', models.BooleanField(blank=True, default=False, null=True, verbose_name='парсер Авито сейчас запущен?')),
                ('parser_link_avito', models.CharField(blank=True, null=True, verbose_name='ссылка Авито')),
                ('parser_last_change_at_avito', models.DateField(blank=True, null=True, verbose_name='дата последнего изменения Авито')),
                ('parser_last_parse_at_avito', models.DateTimeField(blank=True, null=True, verbose_name='дата и время последней загрузки Авито')),
                ('is_first_parsing_zoon', models.BooleanField(blank=True, default=True, null=True, verbose_name='это первый парсинг Zoon?')),
                ('is_parser_run_zoon', models.BooleanField(blank=True, default=False, null=True, verbose_name='парсер Zoon сейчас запущен?')),
                ('parser_link_zoon', models.CharField(blank=True, null=True, verbose_name='ссылка Zoon')),
                ('parser_last_change_at_zoon', models.DateField(blank=True, null=True, verbose_name='дата последнего изменения Zoon')),
                ('parser_last_parse_at_zoon', models.DateTimeField(blank=True, null=True, verbose_name='дата и время последней загрузки Zoon')),
                ('is_first_parsing_flamp', models.BooleanField(blank=True, default=True, null=True, verbose_name='это первый парсинг Flamp?')),
                ('is_parser_run_flamp', models.BooleanField(blank=True, default=False, null=True, verbose_name='парсер Flamp сейчас запущен?')),
                ('parser_link_flamp', models.CharField(blank=True, null=True, verbose_name='ссылка Flamp')),
                ('parser_last_change_at_flamp', models.DateField(blank=True, null=True, verbose_name='дата последнего изменения Flamp')),
                ('parser_last_parse_at_flamp', models.DateTimeField(blank=True, null=True, verbose_name='дата и время последней загрузки Flamp')),
                ('is_first_parsing_yell', models.BooleanField(blank=True, default=True, null=True, verbose_name='это первый парсинг Yell?')),
                ('is_parser_run_yell', models.BooleanField(blank=True, default=False, null=True, verbose_name='парсер Yell сейчас запущен?')),
                ('parser_link_yell', models.CharField(blank=True, null=True, verbose_name='ссылка Yell')),
                ('parser_last_change_at_yell', models.DateField(blank=True, null=True, verbose_name='дата последнего изменения Yell')),
                ('parser_last_parse_at_yell', models.DateTimeField(blank=True, null=True, verbose_name='дата и время последней загрузки Yell')),
                ('is_first_parsing_prodoctorov', models.BooleanField(blank=True, default=True, null=True, verbose_name='это первый парсинг Продокторов?')),
                ('is_parser_run_prodoctorov', models.BooleanField(blank=True, default=False, null=True, verbose_name='парсер Продокторов сейчас запущен?')),
                ('parser_link_prodoctorov', models.CharField(blank=True, null=True, verbose_name='ссылка Продокторов')),
                ('parser_last_change_at_prodoctorov', models.DateField(blank=True, null=True, verbose_name='дата последнего изменения Продокторов')),
                ('parser_last_parse_at_prodoctorov', models.DateTimeField(blank=True, null=True, verbose_name='дата и время последней загрузки Продокторов')),
                ('is_first_parsing_yandex_services', models.BooleanField(blank=True, default=True, null=True, verbose_name='это первый парсинг Яндекс Сервисы?')),
                ('is_parser_run_yandex_services', models.BooleanField(blank=True, default=False, null=True, verbose_name='парсер Яндекс Сервисы сейчас запущен?')),
                ('parser_link_yandex_services', models.CharField(blank=True, null=True, verbose_name='ссылка Яндекс Сервисы')),
                ('parser_last_change_at_yandex_services', models.DateField(blank=True, null=True, verbose_name='дата последнего изменения Яндекс Сервисы')),
                ('parser_last_parse_at_yandex_services', models.DateTimeField(blank=True, null=True, verbose_name='дата и время последней загрузки Яндекс Сервисы')),
                ('is_first_parsing_otzovik', models.BooleanField(blank=True, default=True, null=True, verbose_name='это первый парсинг Отзовик?')),
                ('is_parser_run_otzovik', models.BooleanField(blank=True, default=False, null=True, verbose_name='парсер Отзовик сейчас запущен?')),
                ('parser_link_otzovik', models.CharField(blank=True, null=True, verbose_name='ссылка Отзовик')),
                ('parser_last_change_at_otzovik', models.DateField(blank=True, null=True, verbose_name='дата последнего изменения Отзовик')),
                ('parser_last_parse_at_otzovik', models.DateTimeField(blank=True, null=True, verbose_name='дата и время последней загрузки Отзовик')),
                ('is_first_parsing_irecommend', models.BooleanField(blank=True, default=True, null=True, verbose_name='это первый парсинг Irecommend?')),
                ('is_parser_run_irecommend', models.BooleanField(blank=True, default=False, null=True, verbose_name='парсер Irecommend сейчас запущен?')),
                ('parser_link_irecommend', models.CharField(blank=True, null=True, verbose_name='ссылка Irecommend')),
                ('parser_last_change_at_irecommend', models.DateField(blank=True, null=True, verbose_name='дата последнего изменения Irecommend')),
                ('parser_last_parse_at_irecommend', models.DateTimeField(blank=True, null=True, verbose_name='дата и время последней загрузки Irecommend')),
                ('is_first_parsing_tripadvisor', models.BooleanField(blank=True, default=True, null=True, verbose_name='это первый парсинг Tripadvisor?')),
                ('is_parser_run_tripadvisor', models.BooleanField(blank=True, default=False, null=True, verbose_name='парсер Tripadvisor сейчас запущен?')),
                ('parser_link_tripadvisor', models.CharField(blank=True, null=True, verbose_name='ссылка Tripadvisor')),
                ('parser_last_change_at_tripadvisor', models.DateField(blank=True, null=True, verbose_name='дата последнего изменения Tripadvisor')),
                ('parser_last_parse_at_tripadvisor', models.DateTimeField(blank=True, null=True, verbose_name='дата и время последней загрузки Tripadvisor')),
                ('address', models.CharField(blank=True, null=True, verbose_name='адрес')),
                ('logo', django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='JPEG', keep_meta=True, null=True, quality=75, scale=1, size=[300, 300], upload_to='dashboard/%Y/%m/%d/', verbose_name='логотип')),
                ('name', models.CharField(blank=True, null=True, verbose_name='название')),
                ('phone', models.CharField(blank=True, null=True, verbose_name='телефон')),
                ('feedback_link_yandex', models.CharField(blank=True, null=True, verbose_name='ссылка Яндекс')),
                ('feedback_link_gis', models.CharField(blank=True, null=True, verbose_name='ссылка 2Гис')),
                ('feedback_link_google', models.CharField(blank=True, null=True, verbose_name='ссылка Google')),
                ('feedback_link_avito', models.CharField(blank=True, null=True, verbose_name='ссылка Авито')),
                ('feedback_link_zoon', models.CharField(blank=True, null=True, verbose_name='ссылка Zoon')),
                ('feedback_link_flamp', models.CharField(blank=True, null=True, verbose_name='ссылка Flamp')),
                ('feedback_link_yell', models.CharField(blank=True, null=True, verbose_name='ссылка Yell')),
                ('feedback_link_prodoctorov', models.CharField(blank=True, null=True, verbose_name='ссылка Продокторов')),
                ('feedback_link_yandex_services', models.CharField(blank=True, null=True, verbose_name='ссылка Яндекс услуги')),
                ('feedback_link_otzovik', models.CharField(blank=True, null=True, verbose_name='ссылка Отзовик')),
                ('feedback_link_irecommend', models.CharField(blank=True, null=True, verbose_name='ссылка Irecommend')),
                ('feedback_link_tripadvisor', models.CharField(blank=True, null=True, verbose_name='ссылка Tripadvisor')),
                ('feedback_contact_whatsapp', models.CharField(blank=True, null=True, verbose_name='ссылка Whatsapp')),
                ('feedback_contact_telegram', models.CharField(blank=True, null=True, verbose_name='ссылка Telegram')),
                ('feedback_contact_viber', models.CharField(blank=True, null=True, verbose_name='ссылка Viber')),
                ('feedback_contact_website', models.CharField(blank=True, null=True, verbose_name='ссылка Вебсайт')),
                ('feedback_contact_vk', models.CharField(blank=True, null=True, verbose_name='ссылка VK')),
                ('feedback_contact_ok', models.CharField(blank=True, null=True, verbose_name='ссылка Одноклассники')),
                ('feedback_contact_facebook', models.CharField(blank=True, null=True, verbose_name='ссылка Facebook')),
                ('feedback_contact_instagram', models.CharField(blank=True, null=True, verbose_name='ссылка Instagram')),
                ('feedback_contact_x', models.CharField(blank=True, null=True, verbose_name='ссылка X')),
                ('feedback_contact_youtube', models.CharField(blank=True, null=True, verbose_name='ссылка Youtube')),
                ('feedback_contact_rutube', models.CharField(blank=True, null=True, verbose_name='ссылка Rutube')),
                ('feedback_contact_vimeo', models.CharField(blank=True, null=True, verbose_name='ссылка Vimeo')),
                ('rating_yandex', models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Яндекс')),
                ('rating_gis', models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг 2Гис')),
                ('rating_google', models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Google')),
                ('rating_avito', models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Авито')),
                ('rating_zoon', models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Zoon')),
                ('rating_flamp', models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Flamp')),
                ('rating_yell', models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Yell')),
                ('rating_prodoctorov', models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Продокторов')),
                ('rating_yandex_services', models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Яндекс услуги')),
                ('rating_otzovik', models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Отзовик')),
                ('rating_irecommend', models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Irecommend')),
                ('rating_tripadvisor', models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Tripadvisor')),
            ],
            options={
                'verbose_name': 'филиал',
                'verbose_name_plural': 'филиалы',
                'db_table': 'resources_company',
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_notify_0', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать с 0 звезд?')),
                ('is_notify_1', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать с 1 звездой?')),
                ('is_notify_2', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать с 2 звездами?')),
                ('is_notify_3', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать с 3 звездами?')),
                ('is_notify_4', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать с 4 звездами?')),
                ('is_notify_5', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать с 5 звездами?')),
                ('is_notify_portrate', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать Портрет?')),
                ('is_notify_yandex', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать Яндекс?')),
                ('is_notify_gis', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать 2Гис?')),
                ('is_notify_google', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать Google?')),
                ('is_notify_avito', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать Авито?')),
                ('is_notify_zoon', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать Zoon?')),
                ('is_notify_flamp', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать Flamp?')),
                ('is_notify_yell', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать Yell?')),
                ('is_notify_prodoctorov', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать Продокторов?')),
                ('is_notify_yandex_services', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать Яндекс услуги?')),
                ('is_notify_otzovik', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать Otzovik?')),
                ('is_notify_irecommend', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать Irecommend?')),
                ('is_notify_tripadvisor', models.BooleanField(blank=True, default=True, null=True, verbose_name='оповещать Tripadvisor?')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'участник',
                'verbose_name_plural': 'участники',
                'db_table': 'resources_membership',
            },
        ),
        migrations.AddField(
            model_name='company',
            name='users',
            field=models.ManyToManyField(blank=True, through='resources.Membership', to=settings.AUTH_USER_MODEL, verbose_name='пользователи'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_secret', models.CharField(blank=True, db_index=True, null=True, verbose_name='API ключ')),
                ('balance_currency', djmoney.models.fields.CurrencyField(choices=[('XUA', 'ADB Unit of Account'), ('AFN', 'Afghan Afghani'), ('AFA', 'Afghan Afghani (1927–2002)'), ('ALL', 'Albanian Lek'), ('ALK', 'Albanian Lek (1946–1965)'), ('DZD', 'Algerian Dinar'), ('ADP', 'Andorran Peseta'), ('AOA', 'Angolan Kwanza'), ('AOK', 'Angolan Kwanza (1977–1991)'), ('AON', 'Angolan New Kwanza (1990–2000)'), ('AOR', 'Angolan Readjusted Kwanza (1995–1999)'), ('ARA', 'Argentine Austral'), ('ARS', 'Argentine Peso'), ('ARM', 'Argentine Peso (1881–1970)'), ('ARP', 'Argentine Peso (1983–1985)'), ('ARL', 'Argentine Peso Ley (1970–1983)'), ('AMD', 'Armenian Dram'), ('AWG', 'Aruban Florin'), ('AUD', 'Australian Dollar'), ('ATS', 'Austrian Schilling'), ('AZN', 'Azerbaijani Manat'), ('AZM', 'Azerbaijani Manat (1993–2006)'), ('BSD', 'Bahamian Dollar'), ('BHD', 'Bahraini Dinar'), ('BDT', 'Bangladeshi Taka'), ('BBD', 'Barbadian Dollar'), ('BYN', 'Belarusian Ruble'), ('BYB', 'Belarusian Ruble (1994–1999)'), ('BYR', 'Belarusian Ruble (2000–2016)'), ('BEF', 'Belgian Franc'), ('BEC', 'Belgian Franc (convertible)'), ('BEL', 'Belgian Franc (financial)'), ('BZD', 'Belize Dollar'), ('BMD', 'Bermudan Dollar'), ('BTN', 'Bhutanese Ngultrum'), ('BOB', 'Bolivian Boliviano'), ('BOL', 'Bolivian Boliviano (1863–1963)'), ('BOV', 'Bolivian Mvdol'), ('BOP', 'Bolivian Peso'), ('VED', 'Bolívar Soberano'), ('BAM', 'Bosnia-Herzegovina Convertible Mark'), ('BAD', 'Bosnia-Herzegovina Dinar (1992–1994)'), ('BAN', 'Bosnia-Herzegovina New Dinar (1994–1997)'), ('BWP', 'Botswanan Pula'), ('BRC', 'Brazilian Cruzado (1986–1989)'), ('BRZ', 'Brazilian Cruzeiro (1942–1967)'), ('BRE', 'Brazilian Cruzeiro (1990–1993)'), ('BRR', 'Brazilian Cruzeiro (1993–1994)'), ('BRN', 'Brazilian New Cruzado (1989–1990)'), ('BRB', 'Brazilian New Cruzeiro (1967–1986)'), ('BRL', 'Brazilian Real'), ('GBP', 'British Pound'), ('BND', 'Brunei Dollar'), ('BGL', 'Bulgarian Hard Lev'), ('BGN', 'Bulgarian Lev'), ('BGO', 'Bulgarian Lev (1879–1952)'), ('BGM', 'Bulgarian Socialist Lev'), ('BUK', 'Burmese Kyat'), ('BIF', 'Burundian Franc'), ('XPF', 'CFP Franc'), ('KHR', 'Cambodian Riel'), ('CAD', 'Canadian Dollar'), ('CVE', 'Cape Verdean Escudo'), ('KYD', 'Cayman Islands Dollar'), ('XAF', 'Central African CFA Franc'), ('CLE', 'Chilean Escudo'), ('CLP', 'Chilean Peso'), ('CLF', 'Chilean Unit of Account (UF)'), ('CNX', 'Chinese People’s Bank Dollar'), ('CNY', 'Chinese Yuan'), ('CNH', 'Chinese Yuan (offshore)'), ('COP', 'Colombian Peso'), ('COU', 'Colombian Real Value Unit'), ('KMF', 'Comorian Franc'), ('CDF', 'Congolese Franc'), ('CRC', 'Costa Rican Colón'), ('HRD', 'Croatian Dinar'), ('HRK', 'Croatian Kuna'), ('CUC', 'Cuban Convertible Peso'), ('CUP', 'Cuban Peso'), ('CYP', 'Cypriot Pound'), ('CZK', 'Czech Koruna'), ('CSK', 'Czechoslovak Hard Koruna'), ('DKK', 'Danish Krone'), ('DJF', 'Djiboutian Franc'), ('DOP', 'Dominican Peso'), ('NLG', 'Dutch Guilder'), ('XCD', 'East Caribbean Dollar'), ('DDM', 'East German Mark'), ('ECS', 'Ecuadorian Sucre'), ('ECV', 'Ecuadorian Unit of Constant Value'), ('EGP', 'Egyptian Pound'), ('GQE', 'Equatorial Guinean Ekwele'), ('ERN', 'Eritrean Nakfa'), ('EEK', 'Estonian Kroon'), ('ETB', 'Ethiopian Birr'), ('EUR', 'Euro'), ('XBA', 'European Composite Unit'), ('XEU', 'European Currency Unit'), ('XBB', 'European Monetary Unit'), ('XBC', 'European Unit of Account (XBC)'), ('XBD', 'European Unit of Account (XBD)'), ('FKP', 'Falkland Islands Pound'), ('FJD', 'Fijian Dollar'), ('FIM', 'Finnish Markka'), ('FRF', 'French Franc'), ('XFO', 'French Gold Franc'), ('XFU', 'French UIC-Franc'), ('GMD', 'Gambian Dalasi'), ('GEK', 'Georgian Kupon Larit'), ('GEL', 'Georgian Lari'), ('DEM', 'German Mark'), ('GHS', 'Ghanaian Cedi'), ('GHC', 'Ghanaian Cedi (1979–2007)'), ('GIP', 'Gibraltar Pound'), ('XAU', 'Gold'), ('GRD', 'Greek Drachma'), ('GTQ', 'Guatemalan Quetzal'), ('GWP', 'Guinea-Bissau Peso'), ('GNF', 'Guinean Franc'), ('GNS', 'Guinean Syli'), ('GYD', 'Guyanaese Dollar'), ('HTG', 'Haitian Gourde'), ('HNL', 'Honduran Lempira'), ('HKD', 'Hong Kong Dollar'), ('HUF', 'Hungarian Forint'), ('IMP', 'IMP'), ('ISK', 'Icelandic Króna'), ('ISJ', 'Icelandic Króna (1918–1981)'), ('INR', 'Indian Rupee'), ('IDR', 'Indonesian Rupiah'), ('IRR', 'Iranian Rial'), ('IQD', 'Iraqi Dinar'), ('IEP', 'Irish Pound'), ('ILS', 'Israeli New Shekel'), ('ILP', 'Israeli Pound'), ('ILR', 'Israeli Shekel (1980–1985)'), ('ITL', 'Italian Lira'), ('JMD', 'Jamaican Dollar'), ('JPY', 'Japanese Yen'), ('JOD', 'Jordanian Dinar'), ('KZT', 'Kazakhstani Tenge'), ('KES', 'Kenyan Shilling'), ('KWD', 'Kuwaiti Dinar'), ('KGS', 'Kyrgystani Som'), ('LAK', 'Laotian Kip'), ('LVL', 'Latvian Lats'), ('LVR', 'Latvian Ruble'), ('LBP', 'Lebanese Pound'), ('LSL', 'Lesotho Loti'), ('LRD', 'Liberian Dollar'), ('LYD', 'Libyan Dinar'), ('LTL', 'Lithuanian Litas'), ('LTT', 'Lithuanian Talonas'), ('LUL', 'Luxembourg Financial Franc'), ('LUC', 'Luxembourgian Convertible Franc'), ('LUF', 'Luxembourgian Franc'), ('MOP', 'Macanese Pataca'), ('MKD', 'Macedonian Denar'), ('MKN', 'Macedonian Denar (1992–1993)'), ('MGA', 'Malagasy Ariary'), ('MGF', 'Malagasy Franc'), ('MWK', 'Malawian Kwacha'), ('MYR', 'Malaysian Ringgit'), ('MVR', 'Maldivian Rufiyaa'), ('MVP', 'Maldivian Rupee (1947–1981)'), ('MLF', 'Malian Franc'), ('MTL', 'Maltese Lira'), ('MTP', 'Maltese Pound'), ('MRU', 'Mauritanian Ouguiya'), ('MRO', 'Mauritanian Ouguiya (1973–2017)'), ('MUR', 'Mauritian Rupee'), ('MXV', 'Mexican Investment Unit'), ('MXN', 'Mexican Peso'), ('MXP', 'Mexican Silver Peso (1861–1992)'), ('MDC', 'Moldovan Cupon'), ('MDL', 'Moldovan Leu'), ('MCF', 'Monegasque Franc'), ('MNT', 'Mongolian Tugrik'), ('MAD', 'Moroccan Dirham'), ('MAF', 'Moroccan Franc'), ('MZE', 'Mozambican Escudo'), ('MZN', 'Mozambican Metical'), ('MZM', 'Mozambican Metical (1980–2006)'), ('MMK', 'Myanmar Kyat'), ('NAD', 'Namibian Dollar'), ('NPR', 'Nepalese Rupee'), ('ANG', 'Netherlands Antillean Guilder'), ('TWD', 'New Taiwan Dollar'), ('NZD', 'New Zealand Dollar'), ('NIO', 'Nicaraguan Córdoba'), ('NIC', 'Nicaraguan Córdoba (1988–1991)'), ('NGN', 'Nigerian Naira'), ('KPW', 'North Korean Won'), ('NOK', 'Norwegian Krone'), ('OMR', 'Omani Rial'), ('PKR', 'Pakistani Rupee'), ('XPD', 'Palladium'), ('PAB', 'Panamanian Balboa'), ('PGK', 'Papua New Guinean Kina'), ('PYG', 'Paraguayan Guarani'), ('PEI', 'Peruvian Inti'), ('PEN', 'Peruvian Sol'), ('PES', 'Peruvian Sol (1863–1965)'), ('PHP', 'Philippine Peso'), ('XPT', 'Platinum'), ('PLN', 'Polish Zloty'), ('PLZ', 'Polish Zloty (1950–1995)'), ('PTE', 'Portuguese Escudo'), ('GWE', 'Portuguese Guinea Escudo'), ('QAR', 'Qatari Riyal'), ('XRE', 'RINET Funds'), ('RHD', 'Rhodesian Dollar'), ('RON', 'Romanian Leu'), ('ROL', 'Romanian Leu (1952–2006)'), ('RUB', 'Russian Ruble'), ('RUR', 'Russian Ruble (1991–1998)'), ('RWF', 'Rwandan Franc'), ('SVC', 'Salvadoran Colón'), ('WST', 'Samoan Tala'), ('SAR', 'Saudi Riyal'), ('RSD', 'Serbian Dinar'), ('CSD', 'Serbian Dinar (2002–2006)'), ('SCR', 'Seychellois Rupee'), ('SLE', 'Sierra Leonean Leone'), ('SLL', 'Sierra Leonean Leone (1964—2022)'), ('XAG', 'Silver'), ('SGD', 'Singapore Dollar'), ('SKK', 'Slovak Koruna'), ('SIT', 'Slovenian Tolar'), ('SBD', 'Solomon Islands Dollar'), ('SOS', 'Somali Shilling'), ('ZAR', 'South African Rand'), ('ZAL', 'South African Rand (financial)'), ('KRH', 'South Korean Hwan (1953–1962)'), ('KRW', 'South Korean Won'), ('KRO', 'South Korean Won (1945–1953)'), ('SSP', 'South Sudanese Pound'), ('SUR', 'Soviet Rouble'), ('ESP', 'Spanish Peseta'), ('ESA', 'Spanish Peseta (A account)'), ('ESB', 'Spanish Peseta (convertible account)'), ('XDR', 'Special Drawing Rights'), ('LKR', 'Sri Lankan Rupee'), ('SHP', 'St. Helena Pound'), ('XSU', 'Sucre'), ('SDD', 'Sudanese Dinar (1992–2007)'), ('SDG', 'Sudanese Pound'), ('SDP', 'Sudanese Pound (1957–1998)'), ('SRD', 'Surinamese Dollar'), ('SRG', 'Surinamese Guilder'), ('SZL', 'Swazi Lilangeni'), ('SEK', 'Swedish Krona'), ('CHF', 'Swiss Franc'), ('SYP', 'Syrian Pound'), ('STN', 'São Tomé & Príncipe Dobra'), ('STD', 'São Tomé & Príncipe Dobra (1977–2017)'), ('TVD', 'TVD'), ('TJR', 'Tajikistani Ruble'), ('TJS', 'Tajikistani Somoni'), ('TZS', 'Tanzanian Shilling'), ('XTS', 'Testing Currency Code'), ('THB', 'Thai Baht'), ('TPE', 'Timorese Escudo'), ('TOP', 'Tongan Paʻanga'), ('TTD', 'Trinidad & Tobago Dollar'), ('TND', 'Tunisian Dinar'), ('TRY', 'Turkish Lira'), ('TRL', 'Turkish Lira (1922–2005)'), ('TMT', 'Turkmenistani Manat'), ('TMM', 'Turkmenistani Manat (1993–2009)'), ('USD', 'US Dollar'), ('USN', 'US Dollar (Next day)'), ('USS', 'US Dollar (Same day)'), ('UGX', 'Ugandan Shilling'), ('UGS', 'Ugandan Shilling (1966–1987)'), ('UAH', 'Ukrainian Hryvnia'), ('UAK', 'Ukrainian Karbovanets'), ('AED', 'United Arab Emirates Dirham'), ('UYW', 'Uruguayan Nominal Wage Index Unit'), ('UYU', 'Uruguayan Peso'), ('UYP', 'Uruguayan Peso (1975–1993)'), ('UYI', 'Uruguayan Peso (Indexed Units)'), ('UZS', 'Uzbekistani Som'), ('VUV', 'Vanuatu Vatu'), ('VES', 'Venezuelan Bolívar'), ('VEB', 'Venezuelan Bolívar (1871–2008)'), ('VEF', 'Venezuelan Bolívar (2008–2018)'), ('VND', 'Vietnamese Dong'), ('VNN', 'Vietnamese Dong (1978–1985)'), ('CHE', 'WIR Euro'), ('CHW', 'WIR Franc'), ('XOF', 'West African CFA Franc'), ('YDD', 'Yemeni Dinar'), ('YER', 'Yemeni Rial'), ('YUN', 'Yugoslavian Convertible Dinar (1990–1992)'), ('YUD', 'Yugoslavian Hard Dinar (1966–1990)'), ('YUM', 'Yugoslavian New Dinar (1994–2002)'), ('YUR', 'Yugoslavian Reformed Dinar (1992–1993)'), ('ZWN', 'ZWN'), ('ZRN', 'Zairean New Zaire (1993–1998)'), ('ZRZ', 'Zairean Zaire (1971–1993)'), ('ZMW', 'Zambian Kwacha'), ('ZMK', 'Zambian Kwacha (1968–2012)'), ('ZWD', 'Zimbabwean Dollar (1980–2008)'), ('ZWR', 'Zimbabwean Dollar (2008)'), ('ZWL', 'Zimbabwean Dollar (2009)')], default='RUB', editable=False, max_length=3, null=True)),
                ('balance', djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default=Decimal('0'), default_currency='RUB', max_digits=14, null=True)),
                ('is_billing', models.BooleanField(blank=True, default=False, null=True, verbose_name='списывать оплату?')),
                ('default_timezone', models.CharField(choices=[('UTC', 'UTC'), ('Europe/Moscow', 'Москва'), ('Asia/Yekaterinburg', 'Екатеринбург')], default='UTC', null=True, verbose_name='Временная зона по умолчанию')),
                ('telegram_id', models.CharField(blank=True, null=True, verbose_name='telegram ID')),
                ('rate', models.CharField(choices=[('STARTS', 'Старт'), ('REGULAR', 'Стандарт'), ('BUSINESS', 'Бизнес')], default='STARTS', null=True, verbose_name='Тариф')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'профиль',
                'verbose_name_plural': 'профили',
                'db_table': 'resources_profile',
            },
        ),
        migrations.CreateModel(
            name='VisitStamp',
            fields=[
                ('id', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True, null=True, verbose_name='дата создания')),
                ('utm_source', models.CharField(blank=True, null=True, verbose_name='источник')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.company', verbose_name='филиал')),
            ],
            options={
                'verbose_name': 'Отпечаток перехода на форму запроса отзывов',
                'verbose_name_plural': 'Отпечатки перехода на форму запроса отзывов',
                'db_table': 'resources_visit_stamp',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='дата создания')),
                ('phone', models.CharField(blank=True, null=True, verbose_name='контактный телефон')),
                ('text', models.TextField(blank=True, null=True, verbose_name='текст сообщения')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.company', verbose_name='филиал')),
                ('visit_stamp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.visitstamp', verbose_name='отпечаток перехода на форму запроса отзывов')),
            ],
            options={
                'verbose_name': 'сообщение',
                'verbose_name_plural': 'сообщения',
                'db_table': 'resources_negative_message',
            },
        ),
        migrations.CreateModel(
            name='ClickStamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True, null=True, verbose_name='дата создания')),
                ('service', models.CharField(blank=True, choices=[('PORTRATE', 'Портрет'), ('YANDEX', 'Яндекс'), ('GIS', '2Гис'), ('GOOGLE', 'Google'), ('AVITO', 'Авито'), ('ZOON', 'Zoon'), ('FLAMP', 'Flamp'), ('YELL', 'Yell'), ('PRODOCTOROV', 'Продокторов'), ('YANDEX_SERVICES', 'Яндекс Услуги'), ('OTZOVIK', 'Otzovik'), ('IRECOMMEND', 'Irecommend'), ('TRIPADVISOR', 'Tripadvisor')], default='YANDEX', null=True, verbose_name='сервис')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.company', verbose_name='филиал')),
                ('visit_stamp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.visitstamp', verbose_name='отпечаток перехода на форму запроса отзывов')),
            ],
            options={
                'verbose_name': 'Отпечаток клика по кнопке сервиса на форме запроса отзывов',
                'verbose_name_plural': 'Отпечатки клика по кнопке сервиса на форме запроса отзывов',
                'db_table': 'resources_click_stamp',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(blank=True, null=True, verbose_name='дата создания')),
                ('is_visible', models.BooleanField(blank=True, default=True, null=True, verbose_name='отображается в виджете?')),
                ('is_moderated', models.BooleanField(blank=True, default=False, null=True, verbose_name='отмодерирован?')),
                ('remote_id', models.CharField(blank=True, null=True, verbose_name='ID (агрегация)')),
                ('service', models.CharField(blank=True, choices=[('PORTRATE', 'Портрет'), ('YANDEX', 'Яндекс'), ('GIS', '2Гис'), ('GOOGLE', 'Google'), ('AVITO', 'Авито'), ('ZOON', 'Zoon'), ('FLAMP', 'Flamp'), ('YELL', 'Yell'), ('PRODOCTOROV', 'Продокторов'), ('YANDEX_SERVICES', 'Яндекс Услуги'), ('OTZOVIK', 'Otzovik'), ('IRECOMMEND', 'Irecommend'), ('TRIPADVISOR', 'Tripadvisor')], default='YANDEX', null=True, verbose_name='сервис')),
                ('stars', models.IntegerField(blank=True, default=0, null=True, verbose_name='оценка')),
                ('name', models.CharField(blank=True, null=True, verbose_name='пользователь')),
                ('text', models.TextField(blank=True, null=True, verbose_name='текст отзыва')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.company', verbose_name='филиал')),
            ],
            options={
                'verbose_name': 'отзыв',
                'verbose_name_plural': 'отзывы',
                'db_table': 'resources_review',
                'unique_together': {('company', 'remote_id')},
            },
        ),
    ]
