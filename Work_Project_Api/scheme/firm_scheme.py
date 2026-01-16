from pydantic import (
    BaseModel, 
    PositiveFloat, 
    PositiveInt, 
    NonNegativeInt, 
    field_validator,
    Field
    )
from typing import Optional, Dict, Literal, List, Union
from datetime import datetime

#==========firm/about==========
class FirmAbout(BaseModel):
    information: str

class FirmAboutResponse(BaseModel):
    request_id: str
    status: Literal["success"]
    data: List[FirmAbout]

#==========firm/application?action=about==========
class FirmApplicationAboutDocuments(BaseModel):
    id: Literal["agreement", "license", "conditions", "privacy_policy", "payments"]

class FirmApplicationAboutRequisites(BaseModel):
    key: str
    value: str

class FirmApplicationAboutRequisitesInline(BaseModel):
    entity_name_full: str
    entity_tax_number: str
    entity_number_basis_for_authority: str
    entity_registry_number: str
    entity_address_location: str

class FirmApplicationAbout(BaseModel):
    documents: List[FirmApplicationAboutDocuments]
    support_email: str
    requisites: Optional[List[FirmApplicationAboutRequisites]] = None
    requisites_inline: Optional[FirmApplicationAboutRequisitesInline] = None

class FirmApplicationAboutResponse(BaseModel):
    request_id: str
    status: Literal["success"]
    data: FirmApplicationAbout

#==========firm/application?action=init==========
class FirmApplicationInitInit(BaseModel):
    chain_id: PositiveInt
    zone: str

class FirmApplicationSettings(BaseModel):
    adult_mode: bool
    field_of_activity: str
    geolocation_mode: bool
    dialog_delivery_method: bool
    client_authorization_required: bool

class FirmApplicationColorScheme(BaseModel):
    primary_color: str
    accent_color: str

class FirmApplicationDesktop(BaseModel):
    color_scheme: FirmApplicationColorScheme
    items_image_ratio: str
    infinity_catalog: bool
    full_menu: bool
    auto_change: bool
    name: str
    template: str
    items_max_rows_description: str

class FirmApplicationNamesForAutoChange(BaseModel):
    day: str
    night:str

class FirmApplicationColorSchemeMobile(BaseModel):
    side_menu_background_color: str
    side_menu_icons_and_titles_color: str
    main_color: str

class FirmApplicationCatalog(BaseModel):
    items_in_two_columns: bool
    horizontal_categories: bool
    items_image_ratio: str
    items_max_rows_description: str

class FirmApplicationMobile(BaseModel):
    name: str
    names_for_auto_change: FirmApplicationNamesForAutoChange
    auto_change: bool
    color_scheme: FirmApplicationColorSchemeMobile
    image_resolution: str
    radius_blur: PositiveInt
    template: str
    side_menu_icons_and_titles_bold: bool
    bottom_menu_icons_and_titles_bold: bool
    bottom_menu_titles_show: bool
    catalog: FirmApplicationCatalog
    items_image_ratio: str

class FirmApplicationThemes(BaseModel):
    desktop: FirmApplicationDesktop
    mobile: FirmApplicationMobile

class FirmApplicationAppsLinks(BaseModel):
    universal: str
    ios: str

class FirmApplicationInit(BaseModel):
    init: FirmApplicationInitInit
    name: str
    settings: FirmApplicationSettings
    themes: FirmApplicationThemes
    apps_links: FirmApplicationAppsLinks

class FirmApplicationInitResponse(BaseModel):
    request_id: str
    status: Literal["success"]
    data: FirmApplicationInit

#==========firm/application?action=settings==========
class FirmApplicationThemesSettings(BaseModel):
    field_of_activity: str

class FirmApplicationOptions(BaseModel):
    geolocation_mode: bool
    dialog_delivery_method: bool
    client_authorization_required: bool
    captcha: bool
    authorization_by_telegram: bool

class FirmApplicationSettingsAction(BaseModel):
    theme: FirmApplicationThemesSettings
    options: FirmApplicationOptions

class FirmApplicationSettingsResponse(BaseModel):
    request_id: str
    status: Literal["success"]
    data: FirmApplicationSettingsAction

#==========firm/branch==========
class FirmBranchSender(BaseModel):
    name: Literal["name", "phone_number"]
    required: bool
    type: Literal["string", "phone"]
    length: Literal[50, 20]

class FirmBranchAddress(BaseModel):
    name: Literal["street", "house", "building", "entrance_number", "entrance_code", "floor", "apartment"]
    required: bool
    type: Literal["string", "integer"]
    length: Literal[50, 7, 2, 2, 10, 3, 5]

class FirmBranchAdditional(BaseModel):
    name: Literal["persons", "discount", "change", "comment"]
    required: bool
    type: Literal["integer", "string"]
    length: Literal[3, 20, 10, 200]

class FirmBranchFields(BaseModel):
    name: str
    required: bool
    type: Literal["string", "phone", "email", "integer", "bool"]
    length: Optional[PositiveInt] = None
    group: Literal["sender", "recipient", "address", "additional"]

class FirmBranchSpecialOffersOnMobile(BaseModel):
    separate_section: bool
    title_in_catalog: bool

class FirmBranchOptions(BaseModel):
    block_app: bool
    phone_mask: bool
    special_offers_on_mobile: FirmBranchSpecialOffersOnMobile
    feedback: bool
    order_countdown: bool
    vacancies: bool
    promo_code: bool

class FirmBranchCart(BaseModel):
    lead_time: bool
    notice: str #поле отсутствует в сваге

class FirmBranchSocialNetworks(BaseModel):
    vk: str
    tg: str
    wa: str

class FirmBranchPopular(BaseModel):
    h: str = Field(alias="h1")
    title: str
    keywords: str
    description: str
    text: str
    friendly_url: str
    breadcrumb: str

class FirmBranchRecommend(BaseModel):
    friendly_url: str

class FirmBranchSpecialOffers(BaseModel):
    friendly_url: str
    keywords: str
    description: str
    h: str = Field(alias="h1")
    title: str

class FirmBranchAbout(BaseModel):
    friendly_url: str
    title: str

class FirmBranchFeedback(BaseModel):
    friendly_url: str

class FirmBranchMain(BaseModel):
    h: str = Field(alias="h1")
    breadcrumb: str
    title: str
    keywords: str
    description: str
    text: str

class FirmBranchVacancies(BaseModel):
    friendly_url: str

class FirmBranchSEO(BaseModel):
    popular: FirmBranchPopular
    recommend: FirmBranchRecommend
    special_offers: FirmBranchSpecialOffers = Field(alias="special-offers")
    about: FirmBranchAbout
    feedback: FirmBranchFeedback
    main: FirmBranchMain
    vacancies: FirmBranchVacancies

class FirmBranchInfo(BaseModel):
    options: FirmBranchOptions
    social_networks: FirmBranchSocialNetworks #поле отсутствует в сваге
    notice: str #поле отсутствует в сваге
    cart: FirmBranchCart
    seo: FirmBranchSEO #поле отсутствует в сваге
    yandex_metrika: str #поле отсутствует в сваге

class FirmBranchReferral(BaseModel):
    invited: Union[NonNegativeInt, PositiveInt]
    inviter: Union[NonNegativeInt, PositiveInt]
    percent: Union[NonNegativeInt, PositiveInt]
    pyramid: bool

class FirmBranchAccrual(BaseModel):
    referral: FirmBranchReferral
    withdraw: bool
    decrease: bool
    registration: Union[NonNegativeInt, PositiveInt]
    items: PositiveInt
    feedback: Union[NonNegativeInt, PositiveInt]
    birthday: Union[NonNegativeInt, PositiveInt]

class FirmBranchWithdraw(BaseModel):
    items: PositiveInt

class FirmBranchValidity(BaseModel):
    items: Union[NonNegativeInt, PositiveInt]
    feedback: Union[NonNegativeInt, PositiveInt]
    birthday: Union[NonNegativeInt, PositiveInt]
    registration: Union[NonNegativeInt, PositiveInt]
    referral: PositiveInt

class FirmBranchRules(BaseModel):
    accrual: FirmBranchAccrual
    withdraw: FirmBranchWithdraw
    validity: FirmBranchValidity

class FirmBranchBonuses(BaseModel):
    automation: bool
    enable: bool
    common: bool
    referral: bool
    minimum_sum: bool
    free_delivery: bool
    reports: bool
    hide_accrual: bool
    rules: FirmBranchRules

class FirmBranchDelivery(BaseModel):
    minimum_minutes: Union[NonNegativeInt, PositiveInt]
    maximum_days: PositiveInt

class FirmBranchTimeLimits(BaseModel):
    delivery: FirmBranchDelivery
    pickup: FirmBranchDelivery

class FirmBranchPreorder(BaseModel):
    enable: bool
    only_in_work_time: bool
    always: bool
    time_limits: FirmBranchTimeLimits

class FirmBranchPaymentsOne(BaseModel):
    id: str #Дописать в свагу какие значения могут быть в этом поле
    system_id: str #Дописать в свагу какие значения могут быть в этом поле
    type: str #Дописать в свагу какие значения могут быть в этом поле
    delivery_method: str #Дописать в свагу какие значения могут быть в этом поле

class FirmBranchPaymentsTwo(BaseModel):
    id: str 
    system_id: str
    type: str
    delivery_method: str

class FirmBranchFinalUrls(BaseModel):
    success: List[str]
    fail: List[str]

class FirmBranchInfoPayments(BaseModel):
    method: str
    gateway: str

class FirmBranchPaymentsThree(BaseModel):
    id: str
    system_id: PositiveInt #в сваге - str, в ответе - int
    name: str #Отсутствует в схеме ответа в сваге
    type: str
    final_urls: FirmBranchFinalUrls
    delivery_method: Literal["all", "courier", "pickup"]
    info: FirmBranchInfoPayments

class FirmBranchMap(BaseModel):
    name: str
    key: str

class FirmBranchSettings(BaseModel):
    fields: List[FirmBranchFields] #полностью другая схема ответа этого поля
    info: FirmBranchInfo
    bonuses: FirmBranchBonuses
    preorder: FirmBranchPreorder
    map: FirmBranchMap #Отсутствует в схеме ответа в сваге
    payments: List[Union[FirmBranchPaymentsOne, FirmBranchPaymentsTwo, FirmBranchPaymentsThree]]

class FirmBranchSeo(BaseModel):
    friendly_url: str
    title: Optional[str] = None #Отсутствует в схеме ответа в сваге
    h: Optional[str] = Field(default=None, alias="h1") #Отсутствует в схеме ответа в сваге
    keywords: Optional[str] = None #Отсутствует в схеме ответа в сваге
    description: Optional[str] = None #Отсутствует в схеме ответа в сваге
    text: Optional[str] = None #Отсутствует в схеме ответа в сваге

class FirmBranchTimePeriods(BaseModel):
    splitted: List[str]
    glued: str

class FirmBranchCategories(BaseModel):
    id: str #в сваге - int, в ответе - str
    parent_id: Union[NonNegativeInt, PositiveInt]
    name: str
    date_available: Optional[datetime] = None #Отсутствует в схеме ответа в сваге
    date_expiration: Optional[datetime] = None #Отсутствует в схеме ответа в сваге
    days_of_week: List[Union[PositiveInt, str]] #в сваге указан только один возможный тип ответа
    time_periods: Optional[FirmBranchTimePeriods] = None #Отсутствует в схеме ответа в сваге
    hide_for_districts_ids: Optional[List[PositiveInt]] = None #Отсутствует в схеме ответа в сваге
    published: bool
    seo: FirmBranchSeo

class FirmBranchParameters(BaseModel):
    id: str # в сваге int, в ответе str
    old_cost: Union[NonNegativeInt, str] #Почему в ответе 0 - int, а 10 - строка?
    cost: str # в сваге float, в ответе str
    bonuses: Union[NonNegativeInt, str] #Почему в ответе 0 - int, а 10 - строка?
    proteins: Optional[str] = None # в сваге int, в ответе str
    fats: Optional[str] = None # в сваге int, в ответе str
    carbohydrates: Optional[str] = None # в сваге int, в ответе str
    calories: Optional[str] = None # в сваге int, в ответе str
    vendor_code: Optional[str] = None # в сваге int, в ответе str
    stop_list_enabled: Optional[bool] = None
    modifiers_groups_ids: Optional[List[Union[NonNegativeInt, PositiveInt]]] = None #Отсутствует в схеме ответа в сваге
    description: str

class FirmBranchBonusesSettings(BaseModel):
    accrual: bool
    withdraw: bool

class FirmBranchOptionsItems(BaseModel):
    recommend: bool
    hide_cost_if_zero: bool
    only_informing: bool

class FirmBranchCartSettings(BaseModel):
    minimum_sum: bool
    discount: bool
    free_delivery: bool
    modifiers_multiplier: bool

class FirmBranchSeoItems(BaseModel):
    friendly_url: str
    title: Optional[str] = None #Отсутствует в схеме ответа в сваге
    h: Optional[str] = Field(default=None, alias="h1") #Отсутствует в схеме ответа в сваге
    keywords: Optional[str] = None #Отсутствует в схеме ответа в сваге
    description: Optional[str] = None #Отсутствует в схеме ответа в сваге
    text: Optional[str] = None #Отсутствует в схеме ответа в сваге

class FirmBranchImages(BaseModel):
    small: Optional[str] = None
    medium: Optional[str] = None
    large: Optional[str] = None
    mobile: Optional[str] = None

class FirmBranchItems(BaseModel):
    id: PositiveInt
    name: str
    date_available: Optional[datetime] = None #Отсутствует в схеме ответа в сваге
    date_expiration: Optional[datetime] = None #Отсутствует в схеме ответа в сваге
    days_of_week: List[str] #в сваге int, в ответе str
    time_periods: Optional[FirmBranchTimePeriods] = None
    parameters: List[FirmBranchParameters]
    category_id: str # в сваге int, в ответе str
    description: str
    images: Optional[FirmBranchImages] = None #Отсутствует в схеме ответа в сваге
    labels_ids: Optional[List[PositiveInt]] = None #Отсутствует в схеме ответа в сваге
    bonuses_settings: FirmBranchBonusesSettings
    popular_sort: Union[NonNegativeInt, str] #Почему в ответе 0 - int, а 10 - строка?
    options: FirmBranchOptionsItems
    cart_settings: FirmBranchCartSettings
    published: bool
    hide_for_districts_ids: Optional[List[PositiveInt]] = None
    hide_for_pickups_ids: Optional[List[PositiveInt]] = None
    seo: FirmBranchSeoItems

class FirmBranchModifiers(BaseModel):
    id: str # в сваге int, в ответе str
    name: str
    cost: str # в сваге float, в ответе str
    group_id: str # в сваге int, в ответе str
    proteins: Optional[str] = None #Отсутствует в схеме ответа в сваге
    fats: Optional[str] = None #Отсутствует в схеме ответа в сваге
    carbohydrates: Optional[str] = None #Отсутствует в схеме ответа в сваге
    calories: Optional[str] = None #Отсутствует в схеме ответа в сваге
    vendor_code: Optional[str] = None # в сваге int, в ответе str

class FirmBranchModifiersGroups(BaseModel):
    id: str # в сваге int, в ответе str
    name: str
    type: Literal["all_one", "one_one", "all_unlimited"] #в сваге только - all_one, в ответе больше вариантов
    minimum: str # в сваге int, в ответе str
    maximum: str # в сваге int, в ответе str
    modifiers: List[FirmBranchModifiers]

class FirmBranchLabels(BaseModel):
    id: str
    name: str
    text_color: str
    background_color: str

class FirmBranchSpecialOffersData(BaseModel):
    id: str
    name: str
    date_available: Optional[datetime] = None
    description: Optional[str] = None
    operating_mode: Literal["informing", "automatic_action"]
    authorized_users_enabled: bool
    work_with_pay_bonuses_enabled: bool
    accrual_bonuses_enabled: bool
    first_purchase_enabled: bool
    automatic_old_cost_for_items_enabled: bool
    reuse_enabled: bool
    delivery_method: Literal["all", "courier", "pickup"]
    days_of_week: List[str]
    time_periods: Optional[FirmBranchTimePeriods] = None
    ignore_in_minimum_sum_enabled: bool
    from_to_sums_for_items_from_conditions_enabled: bool
    type: Optional[str] = None
    count_items_for_condition: PositiveInt
    one_item_from_conditions_enabled: bool
    use_only_one_time_in_cart_enabled: bool
    use_only_in_birthday_enabled: bool
    discount: Optional[str] = None
    images: Optional[FirmBranchImages] = None

class FirmBranch(BaseModel):
    settings: FirmBranchSettings
    categories: List[FirmBranchCategories]
    items: List[FirmBranchItems]
    labels: List[FirmBranchLabels] #Отсутствует в схеме ответа в сваге
    modifiers_groups: List[FirmBranchModifiersGroups]
    special_offers: Optional[List[FirmBranchSpecialOffersData]] = None #Отсутствует в схеме ответа в сваге

class FirmBranchResponse(BaseModel):
    request_id: str
    status: Literal["success"]
    data: FirmBranch
    timestamp: PositiveInt

#==========firm/chat?action=message_statuses==========
#не полная документация ответа
class FirmChatMesasageStatusesResponse(BaseModel):
    request_id: str
    status: Literal["success"]
    data: Dict[str, bool]

#==========firm/document==========
class FirmDocumentResponse(BaseModel):
    request_id: str
    status: str
    data: List[str]

#==========firm/couriers?action=info==========
class FirmCouriersInfoText(BaseModel):
    symbol: str
    short: str
    middle: str

class FirmCouriersInfoCurrency(BaseModel):
    code: str
    round: PositiveInt
    text: FirmCouriersInfoText

class FirmCouriersInfoFormats(BaseModel):
    date: str
    cost: str

class FirmCouriersInfoBonus(BaseModel):
    text: str
    round: PositiveInt
    symbol: str

class FirmsCouriersInfoSettings(BaseModel):
    distribution_method: Literal["manually", "automatically"]
    independence: bool
    currency: FirmCouriersInfoCurrency
    formats: FirmCouriersInfoFormats
    bonus: FirmCouriersInfoBonus

class FirmCouriersInfoStatistics(BaseModel):
    orders: PositiveInt
    distance: PositiveInt
    time: PositiveInt

class FirmCouriersInfo(BaseModel):
    name: str
    settings: FirmsCouriersInfoSettings
    status: str
    order_id: PositiveInt
    statistics: FirmCouriersInfoStatistics

class FirmCouriersInfoResponse(BaseModel):
    request_id: str
    status: Literal["success"]
    data: FirmCouriersInfo

#==========firm/couriers?action=orders==========
class FirmCouriersOrdersSettings(BaseModel):
    free_delivery: bool
    minimum_sum: bool
    modifiers_multiplier: bool
    stock_balance: bool

class FirmCouriersOrderItems(BaseModel):
    id: str
    name: str
    description: str
    count: PositiveInt
    cost: str
    settings: FirmCouriersOrdersSettings

class FirmCouriersOrdersCart(BaseModel):
    items: List[FirmCouriersOrderItems]

class FirmCouriersOrders(BaseModel):
    id: str
    order_number: str
    cart: FirmCouriersOrdersCart
    total: str
    sender_name: str
    sender_phone_number: str
    street: str
    house: str
    latitude: PositiveFloat
    longitude: PositiveFloat
    persons: str
    date: str
    status_order: Literal[
        "not_processed", "wait_to_kitchen", "in_kitchen", "cooked", "assembly", "wait_remade", "ready_to_transit", 
        "in_transit", "done", "confirmed", "canceled"
        ]
    prepayment: Literal["paid", "not_paid", "waiting"]
    payment_method: Literal["cash", "online", "card_upon_receipt"]
    delivery_method: Literal["courier", "pickup"]

class FirmCouriersOrdersResponse(BaseModel):
    request_id: str
    status: Literal["success"]
    data: List[FirmCouriersOrders]

#==========firm/feedback?action=cache_fields_default==========
class FirmFeedbackCFDResponse(BaseModel):
    request_id: str
    status: Literal["success"]
    data: List[Union[str, PositiveInt]]

#==========firm/feedback?action=default==========
class FirmFeedbackDefault(BaseModel):
    id: PositiveInt
    date: datetime
    text: str
    status: Literal["positive", "negative"]
    answer: str
    published: bool
    image: str #Отсутствует в схеме ответа в сваге
    name: Optional[str] = None

class FirmFeedbackDefaultResponse(BaseModel):
    request_id: str
    status: Literal["success"]
    data: List[FirmFeedbackDefault]
    timestamp: PositiveInt

#==========firm/feedback?action=orders==========
class FirmFeedbackOrders(BaseModel):
    id: PositiveInt
    number: PositiveInt
    date: datetime

class FirmFeedbackOrdersResponse(BaseModel):
    request_id: str
    status:Literal["success"]
    data: List[FirmFeedbackOrders]

#==========firm/geocoding?action=protocol==========
class FirmGeocodingViewbox(BaseModel):
    field: str
    format: str

class FirmGeocodingMutables(BaseModel):
    country: str
    city: str
    search: str
    viewbox: FirmGeocodingViewbox

class FirmGeocodingConstants(BaseModel):
    bounded: Union[str, NonNegativeInt]
    format: str
    addressdetails: Union[str, NonNegativeInt]
    limit: Union[str, NonNegativeInt]

class FirmGeocodingFields(BaseModel):
    mutables: FirmGeocodingMutables
    constants: FirmGeocodingConstants

class FirmGeocodingFind(BaseModel):
    type: str

class FirmGeocodingLatitudeLongitude(BaseModel):
    action: str
    path: str
    position: Union[NonNegativeInt, PositiveInt]
    type: str

class FirmGeocodingFieldsResponse(BaseModel):
    title: str
    country: str
    city: str
    street: str
    house: str
    zip_code: str
    latitude: str
    longitude: str
    address_line_1: str
    address_line_2: Optional[str] = None

class FirmGeocodingResponse(BaseModel):
    find: FirmGeocodingFind
    fields: FirmGeocodingFieldsResponse

class FirmGeocodingHeaders(BaseModel):
    accept: Literal["application/json"] = Field(alias="Accept")
    Accept_Language: Literal["ru"] = Field(alias="Accept-Language")

class FirmGeocodingSearch(BaseModel):
    url: str
    method: Literal["get"]
    type: Literal["query"]
    headers: FirmGeocodingHeaders
    fields: FirmGeocodingFields
    response: FirmGeocodingResponse

class FirmGeocodingMutablesReverse(BaseModel):
    latitude: str
    longitude: str

class FirmGeocodingConstantsReverse(BaseModel):
    format: str
    addressdetails: str

class FirmGeocodingFieldsReverse(BaseModel):
    mutables: FirmGeocodingMutablesReverse
    constants: FirmGeocodingConstantsReverse

class FirmGeocodingResponseReverse(BaseModel):
    find: FirmGeocodingFind
    fields: FirmGeocodingFieldsResponse

class FirmGeocodingReverse(BaseModel):
    url: str
    method: Literal["get"]
    type: Literal["query"]
    fields: FirmGeocodingFieldsReverse
    response: FirmGeocodingResponseReverse

class FirmGeocoding(BaseModel):
    protected: bool
    search: FirmGeocodingSearch
    reverse: FirmGeocodingReverse
    
class FirmGeocodingResponseResponse(BaseModel):
    request_id: str
    status: Literal["success"]
    data: FirmGeocoding

#==========firm/notifications==========
class FirmNotifications(BaseModel):
    id: str
    date_creation: str
    title: str
    message: str

class FirmNotificationsResponse(BaseModel):
    request_id: str
    status: Literal["success"]
    data: List[FirmNotifications]

#==========firm/order?action=new==========
class MessageSettings(BaseModel):
    minutes: PositiveInt
    permanent_client: bool
    prepayment_order: bool

class FirmOrder(BaseModel):
    message_settings: MessageSettings
    id: PositiveInt
    sum_to_pay: Optional[PositiveInt] = None

class FirmOrderResponse(BaseModel):
    request_id: str
    status: Literal["success"]
    data: FirmOrder #В документации необходимо убрать квадратные скобки списка!

#==========firm/special_offers?action=check_first_purchase==========
class FirmSpecialOffersResponse(BaseModel):
    request_id: str
    status: Literal["success"]
    data: Dict[str, bool]

#==========firm/special_offers?action=get_promo_code==========
class FirmGetPromoCodeTimePeriods(BaseModel):
    splitted: List[str]
    glued: str

class FirmGetPromoCode(BaseModel):
    promo_code: str
    id: str
    name: str
    operating_mode: str
    authorized_users_enabled: bool
    work_with_pay_bonuses_enabled: bool
    accrual_bonuses_enabled: bool
    first_purchase_enabled: bool
    first_purchase_platform: str
    automatic_old_cost_for_items_enabled: bool
    reuse_enabled: bool
    delivery_method: str
    days_of_week: List[Literal["1", "2", "3", "4", "5", "6", "7"]]
    time_periods: FirmGetPromoCodeTimePeriods
    ignore_in_minimum_sum_enabled: bool
    from_to_sums_for_items_from_conditions_enabled: bool
    type: str
    count_items_for_condition: PositiveInt
    one_item_from_conditions_enabled: bool
    use_only_one_time_in_cart_enabled: bool
    use_only_in_birthday_enabled: bool
    discount: str

    @field_validator("days_of_week")
    @classmethod
    def validate_days_of_week(cls, value):
        invalid_days = [day for day in value if day not in ["1", "2", "3", "4", "5", "6", "7"]]
        if invalid_days:
            raise ValueError(f"Некорректное значение в days_of_week - {invalid_days}")
        return value
    
class FirmSpecialOffersGetPromoCodeResponse(BaseModel):
    request_id: str
    status: Literal["success"]
    data: FirmGetPromoCode

    @field_validator("data")
    @classmethod
    def assert_expected_promo_code(cls, v, info):
        expected_promo_code = info.context.get("expected_promo_code", [])
        if expected_promo_code and v.promo_code not in expected_promo_code:
            raise ValueError(f"Ни одно из ожидаемых имен {expected_promo_code} не найдено")
        return v

#==========firm/vacancies==========
class FirmVacanciesGet(BaseModel):
    id: str
    name: str
    description: Optional[str] = None # Необязательное поле
    cause: Optional[str] = None
    # reason: str поле отсутствует в реальном ответе
    count: str
    requirements: Optional[str] = None
    duties: Optional[str] = None
    conditions: Optional[str] = None
    salary: str
    image_preview: str # Обязательное поле
    image_full: str # Обязательное поле

class FirmVacanciesGetResponse(BaseModel):
    request_id: str
    status: Literal["success"]
    data: List[FirmVacanciesGet]
    timestamp: Optional[PositiveInt] = None

#==========Стандартная успешная схема ответов==========
class SuccessData(BaseModel):
    status: str
    timestamp: Optional[PositiveInt] = None

class SuccessResponse(BaseModel):
    request_id: str
    status: Literal["success"]
    data: SuccessData

class SuccessResponseSecound(BaseModel):
    request_id: str
    status: Literal["success"]
    data: List

#==========Стандартная схема ошибок==========
class ErrorDetailsVariables(BaseModel):
    field: Optional[str] = None
    header: Optional[str] = None

class ErrorDetails(BaseModel):
    """Ожидаемая схема ответа при ошибке в блоке error, относится к классу ErrorData"""
    code: PositiveInt
    description: str
    variables: Optional[ErrorDetailsVariables] = None

class ErrorData(BaseModel):
    """Ожидаемая схема ответа при ожидаемой ошибке. Применимо к любому методу, при невалидном запросе"""
    request_id: str
    status: Literal["error"]
    error: ErrorDetails
