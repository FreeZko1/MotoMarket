from flask import Blueprint, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired

# Blueprint setup
"""
class VehicleForm(FlaskForm):
    budget = RadioField(
        'Jaký je váš rozpočet na nové vozidlo?',
        choices=[
            ('<200000', 'Méně než 200,000 Kč'),
            ('200000-500000', '200,000 - 500,000 Kč'),
            ('500000-800000', '500,000 - 800,000 Kč'),
            ('>800000', 'Více než 800,000 Kč')
        ],
        validators=[DataRequired()]
    )
    usage_frequency = RadioField(
        'Jak často plánujete používat vozidlo?',
        choices=[
            ('daily', 'Denně'),
            ('several_times_a_week', 'Několikrát týdně'),
            ('weekly', 'Týdně'),
            ('less_often', 'Méně často')
        ],
        validators=[DataRequired()]
    )
    terrain_type = RadioField(
        'Pro jaký typ terénu převážně vozidlo použijete?',
        choices=[
            ('city', 'Město'),
            ('highway', 'Dálnice'),
            ('mixed', 'Smíšený terén'),
            ('offroad', 'Horský nebo terénní')
        ],
        validators=[DataRequired()]
    )
    passengers = RadioField(
        'Kolik lidí obvykle bude cestovat ve vozidle?',
        choices=[
            ('just_me', 'Jen já'),
            ('two_three', '2-3 osoby'),
            ('four_five', '4-5 osob'),
            ('more_than_five', 'Více než 5 osob')
        ],
        validators=[DataRequired()]
    )
    fuel_type = RadioField(
        'Jaký typ paliva preferujete?',
        choices=[
            ('petrol', 'Benzín'),
            ('diesel', 'Diesel'),
            ('electric', 'Elektrický'),
            ('hybrid', 'Hybridní')
        ],
        validators=[DataRequired()]
    )
    eco_importance = RadioField(
        'Jak důležitá je pro vás ekologická udržitelnost vozidla?',
        choices=[
            ('most_important', 'Nejdůležitější'),
            ('important', 'Důležitá'),
            ('neutral', 'Neutrální'),
            ('not_important', 'Není pro mě důležitá')
        ],
        validators=[DataRequired()]
    )
    brand_preference = RadioField(
        'Jakou značku vozidla preferujete?',
        choices=[
            ('skoda', 'Škoda'),
            ('volkswagen', 'Volkswagen'),
            ('toyota', 'Toyota'),
            ('no_preference', 'Nezáleží mi na značce')
        ],
        validators=[DataRequired()]
    )
    cargo_space = RadioField(
        'Jaké jsou vaše požadavky na zavazadlový prostor?',
        choices=[
            ('very_large', 'Velmi velký'),
            ('medium', 'Střední'),
            ('small', 'Malý'),
            ('not_important', 'Není pro mě důležitý')
        ],
        validators=[DataRequired()]
    )
    vehicle_performance = RadioField(
        'Jakou prioritu dáváte výkonu vozidla?',
        choices=[
            ('very_high', 'Velmi vysokou'),
            ('high', 'Vysokou'),
            ('medium', 'Střední'),
            ('low', 'Nízkou')
        ],
        validators=[DataRequired()]
    )
    color_preference = RadioField(
        'Jakou barvu vozidla byste preferovali?',
        choices=[
            ('black', 'Černá'),
            ('white', 'Bílá'),
            ('metallic', 'Metalíza'),
            ('any', 'Jakákoli barva')
        ],
        validators=[DataRequired()]
    )
    ownership_duration = RadioField(
        'Jak dlouho plánujete vozidlo vlastnit?',
        choices=[
            ('<3_years', 'Méně než 3 roky'),
            ('3-5_years', '3-5 let'),
            ('5-10_years', '5-10 let'),
            ('>10_years', 'Více než 10 let')
        ],
        validators=[DataRequired()]
    )
    safety_features = RadioField(
        'Jak důležité jsou pro vás bezpečnostní prvky?',
        choices=[
            ('very_important', 'Velmi důležité'),
            ('important', 'Důležité'),
            ('neutral', 'Neutrální'),
            ('not_important', 'Není pro mě prioritou')
        ],
        validators=[DataRequired()]
    )
    long_distance_travel = RadioField(
        'Jak často cestujete na dlouhé vzdálenosti?',
        choices=[
            ('often', 'Často'),
            ('sometimes', 'Občas'),
            ('rarely', 'Zřídka'),
            ('never', 'Nikdy')
        ],
        validators=[DataRequired()]
    )
    comfort_level = RadioField(
        'Jakou úroveň komfortu očekáváte od vozidla?',
        choices=[
            ('very_high', 'Velmi vysokou'),
            ('high', 'Vysokou'),
            ('medium', 'Střední'),
            ('low', 'Nízkou')
        ],
        validators=[DataRequired()]
    )
    speed_importance = RadioField(
        'Jak důležitá je pro vás rychlost a zrychlení vozidla?',
        choices=[
            ('very_important', 'Velmi důležitá'),
            ('important', 'Důležitá'),
            ('neutral', 'Neutrální'),
            ('not_important', 'Není důležitá')
        ],
        validators=[DataRequired()]
    )
    city_usage_frequency = RadioField(
        'Jak často plánujete vozidlo používat ve městské zástavbě?',
        choices=[
            ('daily', 'Denně'),
            ('often', 'Často'),
            ('sometimes', 'Občas'),
            ('rarely', 'Zřídka')
        ],
        validators=[DataRequired()]
    )
    transmission_preference = RadioField(
        'Preferujete automatickou nebo manuální převodovku?',
        choices=[
            ('automatic', 'Automatickou'),
            ('manual', 'Manuální'),
            ('no_preference', 'Nezáleží'),
            ('unsure', 'Nejsem si jistý')
        ],
        validators=[DataRequired()]
    )
    appearance_importance = RadioField(
        'Jak důležitý je pro vás vzhled vozidla?',
        choices=[
            ('very_important', 'Velmi důležitý'),
            ('important', 'Důležitý'),
            ('neutral', 'Neutrální'),
            ('not_important', 'Není pro mě důležitý')
        ],
        validators=[DataRequired()]
    )
    rough_terrain_usage = RadioField(
        'Jak často plánujete vozidlo používat na nerovném terénu?',
        choices=[
            ('often', 'Často'),
            ('sometimes', 'Občas'),
            ('rarely', 'Zřídka'),
            ('never', 'Nikdy')
        ],
        validators=[DataRequired()]
    )
    drive_type_preference = RadioField(
        'Jaký typ pohonu kola preferujete?',
        choices=[
            ('front_wheel', 'Přední'),
            ('rear_wheel', 'Zadní'),
            ('four_wheel', '4x4'),
            ('no_preference', 'Nezáleží mi na tom')
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Doporučit vozidlo')


@vehicle_advisor.route('/vehicle', methods=['GET', 'POST'])
def vehicle():
    form = VehicleForm()
    if form.validate_on_submit():
        # Příprava dat pro přesměrování
        response_data = {
            'budget': form.budget.data,
            'usage_frequency': form.usage_frequency.data,
            'terrain_type': form.terrain_type.data,
            'passengers': form.passengers.data,
            'fuel_type': form.fuel_type.data,
            'eco_importance': form.eco_importance.data,
            'brand_preference': form.brand_preference.data,
            'cargo_space': form.cargo_space.data,
            'vehicle_performance': form.vehicle_performance.data,
            'color_preference': form.color_preference.data,
            'ownership_duration': form.ownership_duration.data,
            'safety_features': form.safety_features.data,
            'long_distance_travel': form.long_distance_travel.data,
            'comfort_level': form.comfort_level.data,
            'speed_importance': form.speed_importance.data,
            'city_usage_frequency': form.city_usage_frequency.data,
            'transmission_preference': form.transmission_preference.data,
            'appearance_importance': form.appearance_importance.data,
            'rough_terrain_usage': form.rough_terrain_usage.data,
            'drive_type_preference': form.drive_type_preference.data
        }
        # Přesměrujte na stránku s výsledky, posílejte odpovědi jako parametry URL
        query_string = '&'.join([f'{key}={value}' for key, value in response_data.items()])
        return redirect(url_for('vehicle_advisor.result') + '?' + query_string)
    return render_template('vehicle_form.html', form=form)

@vehicle_advisor.route('/result')
def result():
    # Získání všech parametrů z URL
    budget = request.args.get('budget')
    usage_frequency = request.args.get('usage_frequency')
    terrain_type = request.args.get('terrain_type')
    passengers = request.args.get('passengers')
    fuel_type = request.args.get('fuel_type')
    eco_importance = request.args.get('eco_importance')
    brand_preference = request.args.get('brand_preference')
    cargo_space = request.args.get('cargo_space')
    vehicle_performance = request.args.get('vehicle_performance')
    color_preference = request.args.get('color_preference')
    ownership_duration = request.args.get('ownership_duration')
    safety_features = request.args.get('safety_features')
    long_distance_travel = request.args.get('long_distance_travel')
    comfort_level = request.args.get('comfort_level')
    speed_importance = request.args.get('speed_importance')
    city_usage_frequency = request.args.get('city_usage_frequency')
    transmission_preference = request.args.get('transmission_preference')
    appearance_importance = request.args.get('appearance_importance')
    rough_terrain_usage = request.args.get('rough_terrain_usage')
    drive_type_preference = request.args.get('drive_type_preference')

    # Základní logika pro výběr vozidla
    if terrain_type == 'offroad':
        vehicle_recommendation = 'SUV nebo offroad vozidlo'
    elif passengers == 'more_than_five':
        vehicle_recommendation = 'Minivan nebo velké SUV'
    elif fuel_type == 'electric' and eco_importance == 'most_important':
        vehicle_recommendation = 'Elektrické vozidlo'
    elif budget == '<200000' and usage_frequency == 'daily':
        vehicle_recommendation = 'Ekonomické malé vozidlo'
    else:
        vehicle_recommendation = 'Standardní osobní auto'

    # Předání doporučení a všech parametrů do šablony
    return render_template('vehicle_result.html', 
                           recommendation=vehicle_recommendation,
                           budget=budget,
                           usage_frequency=usage_frequency,
                           terrain_type=terrain_type,
                           passengers=passengers,
                           fuel_type=fuel_type,
                           eco_importance=eco_importance,
                           brand_preference=brand_preference,
                           cargo_space=cargo_space,
                           vehicle_performance=vehicle_performance,
                           color_preference=color_preference,
                           ownership_duration=ownership_duration,
                           safety_features=safety_features,
                           long_distance_travel=long_distance_travel,
                           comfort_level=comfort_level,
                           speed_importance=speed_importance,
                           city_usage_frequency=city_usage_frequency,
                           transmission_preference=transmission_preference,
                           appearance_importance=appearance_importance,
                           rough_terrain_usage=rough_terrain_usage,
                           drive_type_preference=drive_type_preference)
"""
