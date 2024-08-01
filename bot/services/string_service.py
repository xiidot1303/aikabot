from bot.services.language_service import *
from app.services.visit_service import VISIT_TYPE, Visit
from app.services.doctor_service import *
from app.services.pharmacy_service import *
from app.services.partner_service import *
from app.utils import generate_google_map_link

async def confirm_visit_string(update, data):
    visit_type = data['visit_type']
    match visit_type:
        case VISIT_TYPE.doctor:
            doctor_id = data['doctor_id']
            doctor: Doctor = await get_doctor_by_id(doctor_id)
            text = f"<b>{await get_word('visit to the doctor', update)}</b>\n\n" \
                f"{Doctor._meta.get_field('name').verbose_name}: <i>{doctor.name}</i>\n" \
                    f"{Doctor._meta.get_field('workplace').verbose_name}: <i>{doctor.workplace}</i>\n\n"

        case VISIT_TYPE.pharmacy:
            pharmacy_id = data['pharmacy_id']
            pharmacy: Pharmacy = await get_pharmacy_by_id(pharmacy_id)
            text = f"<b>{await get_word('visit to the pharmacy', update)}</b>\n\n" \
                f"{Pharmacy._meta.get_field('title').verbose_name}: <i>{pharmacy.title}</i>\n" \
                    f"{Pharmacy._meta.get_field('address').verbose_name}: <i>{pharmacy.address}</i>\n\n"

        case VISIT_TYPE.partners:
            partner_id = data['partner_id']
            partner: Partner = await get_partner_by_id(partner_id)
            text = f"<b>{await get_word('visit to the partners', update)}</b>\n\n" \
                f"{Partner._meta.get_field('name').verbose_name}: <i>{partner.name}</i>\n\n"

    text += f"<b>{await get_word('confirm visit?', update)}</b>"
    return text

async def new_visit_info_string(visit: Visit):
    match visit.type:
        case VISIT_TYPE.doctor:
            doctor: Doctor = await visit.get_address()
            heading = lang_dict["new visit to the doctor"][1]
            text = f"<b>{heading}</b>\n\n🕔 {visit.datetime.strftime("%d.%m.%Y %H:%M:%S")}\n" \
                f"👤 {(await visit.get_bot_user()).name}\n📞 {(await visit.get_bot_user()).phone}\n\n" \
                    f"{Doctor._meta.get_field('name').verbose_name}: {doctor.name}\n" \
                        f"{Doctor._meta.get_field('contact').verbose_name}: {doctor.contact}\n" \
                            f"{Doctor._meta.get_field('direction').verbose_name}: {doctor.direction}\n" \
                                f"{Doctor._meta.get_field('workplace').verbose_name}: {doctor.workplace}\n\n"

        case VISIT_TYPE.pharmacy:
            heading = lang_dict["new visit to the pharmacy"][1]
            pharmacy: Pharmacy = await visit.get_address()
            text = f"<b>{heading}</b>\n\n🕔 {visit.datetime.strftime("%d.%m.%Y %H:%M:%S")}\n" \
                f"👤 {(await visit.get_bot_user()).name}\n📞 {(await visit.get_bot_user()).phone}\n\n" \
                    f"{Pharmacy._meta.get_field('name').verbose_name}: {pharmacy.name}\n" \
                        f"{Pharmacy._meta.get_field('contact').verbose_name}: {pharmacy.contact}\n" \
                            f"{Pharmacy._meta.get_field('title').verbose_name}: {pharmacy.title}\n" \
                                f"{Pharmacy._meta.get_field('address').verbose_name}: {pharmacy.address}\n" \

        case VISIT_TYPE.partners:
            heading = lang_dict["new meeting with partners"][1]
    
    map_link = await generate_google_map_link(visit.lat, visit.lon)
    location_text = visit.location if visit.location else map_link
    text += f"<a href='{map_link}'>{location_text}</a>"
    return text

