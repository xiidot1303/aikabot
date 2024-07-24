from bot.services.language_service import *
from app.services.visit_service import VISIT_TYPE
from app.services.doctor_service import *
from app.services.pharmacy_service import *
from app.services.partner_service import *

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