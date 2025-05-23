# База данных «База данных учёта залогов автомобилей»

#### Задача – информационная поддержка деятельности автоломбарда.

#### База данных предназначена для:
• ведения списка клиентов;<br>
• управления автомобилями, переданными в залог;<br>
• учета залоговых сделок;<br>
• контроля выплат по залогам;<br>
• управления филиалами и сотрудниками;<br>
• хранения фотографий автомобилей.<br>

#### Необходимо предусмотреть:
1. Получение списка автомобилей, принадлежащих конкретному клиенту.
2. Отслеживание текущих залогов для конкретного филиала или сотрудника.
3. Расчет суммы задолженности клиента по активным залогам (с учетом процентов).
4. Определение автомобилей, срок залога которых истек (для последующей реализации).
5. Формирование отчета по истории платежей по конкретному залогу.
6. Учет количества залогов, оформленных каждым сотрудником.

#### Пояснения
VIN-номер автомобиля: Уникальный идентификатор (17 символов), используемый для однозначной идентификации автомобиля.
Статусы залогов:

Активный — клиент обслуживает залог (вносит платежи).<br>
Выкуплен — клиент погасил задолженность и забрал автомобиль.<br>
Продан — срок залога истек, автомобиль реализован.<br>
Связь "Сотрудник — Филиал": Каждый сотрудник привязан к одному филиалу, но один филиал может иметь множество сотрудников.<br>
Фотографии автомобилей: Хранятся для визуальной идентификации и оценки состояния авто при приеме/выдаче.<br>

## Описание ER-модели
#### Клиенты (clients)
Атрибуты: client_id, ФИО, дата рождения, паспортные данные, адрес, телефон, email.<br>
Связи: Клиент может иметь несколько автомобилей (cars.client_id).
#### Автомобили (cars)
Атрибуты: car_id, vin (уникальный), марка, модель, год выпуска, цвет, пробег, мощность двигателя, тип топлива.<br>
Связи: Привязан к клиенту (clients.client_id), может участвовать в одном залоге (pledges.car_id).
#### Филиалы автоломбардов (pawnshops)
Атрибуты: pawnshop_id, название, адрес, контакты, рабочие часы.<br>
Связи: Связан с сотрудниками (employees.pawnshop_id) и залогами (pledges.pawnshop_id).
#### Сотрудники (employees)
Атрибуты: employee_id, ФИО, должность, дата найма, контакты.<br>
Связи: Привязан к филиалу (pawnshops.pawnshop_id), оформляет залоги (pledges.employee_id) и обрабатывает платежи (payments.employee_id).
#### Залоги (pledges)
Атрибуты: pledge_id, дата залога, дата окончания, сумма, процентная ставка, статус (активный/выкуплен/продан).<br>
Связи: Связан с автомобилем (cars.car_id), филиалом (pawnshops.pawnshop_id) и сотрудником (employees.employee_id).
#### Платежи (payments)
Атрибуты: payment_id, дата платежа, сумма, тип (частичная выплата/полный выкуп).<br>
Связи: Привязан к залогу (pledges.pledge_id) и сотруднику (employees.employee_id).
#### Фотографии автомобилей (car_photos)
Атрибуты: photo_id, URL фотографии, дата загрузки.<br>
Связи: Связан с автомобилем (cars.car_id).
