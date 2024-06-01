from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import FteJustification
from django.http import JsonResponse
import json

def calculate_research_cost(patient_count, revenue_per_patient, startup_fee, indirect_cost, trial_count, standard_care_factor):

    research_monthly = round((patient_count * revenue_per_patient + startup_fee) * (1 + indirect_cost) * trial_count)
    research_yearly = round(research_monthly * 12)
    standard_care_monthly = round(research_monthly * (1 + standard_care_factor))
    standard_care_yearly = round(standard_care_monthly * 12)
    return research_monthly, research_yearly, standard_care_monthly, standard_care_yearly

def calculate_staff_and_profit(solid_research_yearly, heme_research_yearly, nurse_expert_count, salary_nurse_expert, nurse_intermediate_count, salary_nurse_intermediate, nurse_novice_count, salary_nurse_novice, crc_expert_count, salary_crc_expert, crc_intermediate_count, salary_crc_intermediate, crc_novice_count, salary_crc_novice, benefit_cost, admin_staffing):
    print(solid_research_yearly, heme_research_yearly, nurse_expert_count, salary_nurse_expert, nurse_intermediate_count, salary_nurse_intermediate, nurse_novice_count, salary_nurse_novice, crc_expert_count, salary_crc_expert, crc_intermediate_count, salary_crc_intermediate, crc_novice_count, salary_crc_novice, benefit_cost, admin_staffing)
    staff_cost_primary = round((nurse_expert_count * salary_nurse_expert + nurse_intermediate_count * salary_nurse_intermediate + nurse_novice_count * salary_nurse_novice + crc_expert_count * salary_crc_expert + crc_intermediate_count * salary_crc_intermediate + crc_novice_count * salary_crc_novice) * (1 + benefit_cost))
    staff_cost_admin = round(staff_cost_primary * admin_staffing)
    potential_profit_yearly = round(solid_research_yearly + heme_research_yearly - staff_cost_primary - staff_cost_admin)
    return staff_cost_primary, staff_cost_admin, potential_profit_yearly


def fte_justification(request):

    solid_trial = solid_patient = heme_trial = heme_patient = 1
    solid_revenue_per_patient = 60000
    heme_revenue_per_patient = 90000
    solid_startup_fee = 20000
    heme_startup_fee = 20000
    solid_indirect_cost = 0.30
    heme_indirect_cost = 0.30
    solid_acuity = 30
    heme_acuity = 30

    nurse_expert_count = 1
    nurse_intermediate_count = 0
    nurse_novice_count = 0

    crc_expert_count = 1
    crc_intermediate_count = 0
    crc_novice_count = 0


    salary_nurse_expert = 100000
    salary_nurse_intermediate = 75000
    salary_nurse_novice = 60000

    salary_crc_expert = 80000
    salary_crc_intermediate = 65000
    salary_crc_novice = 55000

    benefit_cost = 0.30
    admin_staffing = 0.30
    standard_care_factor = 0.30

    solid_research_monthly, solid_research_yearly, solid_standard_care_monthly, solid_standard_care_yearly = calculate_research_cost(
        solid_patient, solid_revenue_per_patient, solid_startup_fee, solid_indirect_cost, solid_trial, standard_care_factor
    )

    heme_research_monthly, heme_research_yearly, heme_standard_care_monthly, heme_standard_care_yearly = calculate_research_cost(
        heme_patient, heme_revenue_per_patient, heme_startup_fee, heme_indirect_cost, heme_trial, standard_care_factor
    )

    staff_cost_primary, staff_cost_admin, potential_profit_yearly = calculate_staff_and_profit(
        solid_research_yearly, heme_research_yearly, nurse_expert_count, salary_nurse_expert, nurse_intermediate_count, salary_nurse_intermediate, nurse_novice_count, salary_nurse_novice, crc_expert_count, salary_crc_expert, crc_intermediate_count, salary_crc_intermediate, crc_novice_count, salary_crc_novice, benefit_cost, admin_staffing
    )
    context = {
        'data':{
            'solid_trial': solid_trial,
            'solid_patient': solid_patient,
            'heme_trial': heme_trial,
            'heme_patient': heme_patient,
            'solid_research_monthly': solid_research_monthly,
            'solid_research_yearly': solid_research_yearly,
            'solid_standard_care_monthly': solid_standard_care_monthly,
            'solid_standard_care_yearly': solid_standard_care_yearly,
            'heme_research_monthly': heme_research_monthly,
            'heme_research_yearly': heme_research_yearly,
            'heme_standard_care_monthly': heme_standard_care_monthly,
            'heme_standard_care_yearly': heme_standard_care_yearly,
            'nurse_expert_count': nurse_expert_count,
            'nurse_intermediate_count': nurse_intermediate_count,
            'nurse_novice_count': nurse_novice_count,
            'crc_expert_count': crc_expert_count,
            'crc_intermediate_count': crc_intermediate_count,
            'crc_novice_count': crc_novice_count,
            'staff_cost_primary': staff_cost_primary,
            'staff_cost_admin': staff_cost_admin,
            'potential_profit_yearly': potential_profit_yearly,
            'solid_revenue_per_patient': solid_revenue_per_patient,
            'solid_startup_fee': solid_startup_fee,
            'solid_indirect_cost': solid_indirect_cost,
            'standard_care_factor': standard_care_factor,
            'heme_revenue_per_patient': heme_revenue_per_patient,
            'heme_startup_fee': heme_startup_fee,
            'heme_indirect_cost': heme_indirect_cost,
            'salary_nurse_expert': salary_nurse_expert,
            "salary_nurse_intermediate": salary_nurse_intermediate,
            "salary_nurse_novice": salary_nurse_novice,
            "salary_crc_expert": salary_crc_expert,
            "salary_crc_intermediate": salary_crc_intermediate,
            "salary_crc_novice": salary_crc_novice,
            'benefit_cost': benefit_cost,
            'admin_staffing': admin_staffing

        }
    }

    return render(request, 'fte_justification.html', context)

@csrf_exempt
def add_fte_justification(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Extract data from POST request
        try:
            

            data = json.loads(request.body)

            solid_trial = data.get('solid_trial')
            solid_patient = data.get('solid_patient')
            heme_trial = data.get('heme_trial')
            heme_patient = data.get('heme_patient')

            solid_revenue_per_patient = data.get('solid_revenue_per_patient')
            solid_startup_fee = data.get('solid_startup_fee')
            solid_indirect_cost = data.get('solid_indirect_cost')
            standard_care_factor = data.get('standard_care_factor')
            heme_revenue_per_patient = data.get('heme_revenue_per_patient')
            heme_startup_fee = data.get('heme_startup_fee')
            heme_indirect_cost = data.get('heme_indirect_cost')
            salary_nurse_expert = data.get('salary_nurse_expert')
            salary_nurse_intermediate = data.get('salary_nurse_intermediate')
            salary_nurse_novice = data.get('salary_nurse_novice')
            salary_crc_expert = data.get('salary_crc_expert')
            salary_crc_intermediate = data.get('salary_crc_intermediate')
            salary_crc_novice = data.get('salary_crc_novice')
            benefit_cost = data.get('benefit_cost')
            admin_staffing = data.get('admin_staffing')

            solid_research_monthly = data.get('solid_research_monthly')
            solid_research_yearly = data.get('solid_research_yearly')
            heme_research_monthly = data.get('heme_research_monthly')
            heme_research_yearly = data.get('heme_research_yearly')
            solid_standard_care_monthly = data.get('solid_standard_care_monthly')
            solid_standard_care_yearly = data.get('solid_standard_care_yearly')
            heme_standard_care_monthly = data.get('heme_standard_care_monthly')
            heme_standard_care_yearly = data.get('heme_standard_care_yearly')
            nurse_expert_count = data.get('nurse_expert_count')
            nurse_intermediate_count = data.get('nurse_intermediate_count')
            nurse_novice_count = data.get('nurse_novice_count')

            crc_expert_count = data.get('crc_expert_count')
            crc_intermediate_count = data.get('crc_intermediate_count')
            crc_novice_count = data.get('crc_novice_count')

            staff_cost_primary = data.get('staff_cost_primary')
            staff_cost_admin = data.get('staff_cost_admin')
            potential_profit_yearly = data.get('potential_profit_yearly')
            
            potential_profit_yearly = data.get('potential_profit_yearly')

            

            solid_research_monthly, solid_research_yearly, solid_standard_care_monthly, solid_standard_care_yearly = calculate_research_cost(
                solid_patient, solid_revenue_per_patient, solid_startup_fee, solid_indirect_cost, solid_trial, standard_care_factor
            )

            heme_research_monthly, heme_research_yearly, heme_standard_care_monthly, heme_standard_care_yearly = calculate_research_cost(
                heme_patient, heme_revenue_per_patient, heme_startup_fee, heme_indirect_cost, heme_trial, standard_care_factor
            )
            staff_cost_primary, staff_cost_admin, potential_profit_yearly = calculate_staff_and_profit(
                solid_research_yearly, heme_research_yearly, nurse_expert_count, salary_nurse_expert, nurse_intermediate_count, salary_nurse_intermediate, nurse_novice_count, salary_nurse_novice, crc_expert_count, salary_crc_expert, crc_intermediate_count, salary_crc_intermediate, crc_novice_count, salary_crc_novice, benefit_cost, admin_staffing
            )
            context = {
                'data':{
                    'solid_trial': solid_trial,
                    'solid_patient': solid_patient,
                    'heme_trial': heme_trial,
                    'heme_patient': heme_patient,
                    'solid_research_monthly': solid_research_monthly,
                    'solid_research_yearly': solid_research_yearly,
                    'solid_standard_care_monthly': solid_standard_care_monthly,
                    'solid_standard_care_yearly': solid_standard_care_yearly,
                    'heme_research_monthly': heme_research_monthly,
                    'heme_research_yearly': heme_research_yearly,
                    'heme_standard_care_monthly': heme_standard_care_monthly,
                    'heme_standard_care_yearly': heme_standard_care_yearly,
                    'nurse_expert_count': nurse_expert_count,
                    'nurse_intermediate_count': nurse_intermediate_count,
                    'nurse_novice_count': nurse_novice_count,
                    'crc_expert_count': crc_expert_count,
                    'crc_intermediate_count': crc_intermediate_count,
                    'crc_novice_count': crc_novice_count,
                    'staff_cost_primary': staff_cost_primary,
                    'staff_cost_admin': staff_cost_admin,
                    'potential_profit_yearly': potential_profit_yearly,
            
                }
            }

            fte_justification = FteJustification.objects.create(
                solid_trial=solid_trial,
                solid_patient=solid_patient,
                heme_trial=heme_trial,
                heme_patient=heme_patient,
                research_solid_monthly=solid_research_monthly,
                research_solid_yearly=solid_research_yearly,
                research_heme_monthly=heme_research_monthly,
                research_heme_yearly=heme_research_yearly,
                care_solid_monthly=solid_standard_care_monthly,
                care_solid_yearly=solid_standard_care_yearly,
                care_heme_monthly=heme_standard_care_monthly,
                care_heme_yearly=heme_standard_care_yearly,
                staff_cost_primary=staff_cost_primary,
                staff_cost_admin=staff_cost_admin,
                potential_profit_yearly=potential_profit_yearly
            )

            return JsonResponse(context) 
        
        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Error decoding JSON data.'}, status=400)
    
    return JsonResponse({'message': 'Invalid request.'}, status=400)

