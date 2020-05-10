from django.db import models


class MUser(models.Model):
    user_code = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=40)
    regist_date = models.DateField()
    regist_user_code = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        db_column="regist_user_code",
        related_name="m_user_regist_user_code",
    )
    update_date = models.DateField()
    update_user_code = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        db_column="update_user_code",
        related_name="m_user_update_user_code",
    )
    last_name = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "m_user"


class MBank(models.Model):
    bank_code = models.CharField(primary_key=True, max_length=4)
    bank_name = models.CharField(max_length=40)
    regist_date = models.DateField()
    regist_user_code = models.ForeignKey(
        "MUser",
        models.DO_NOTHING,
        db_column="regist_user_code",
        related_name="m_bank_regist_user_code",
    )
    update_date = models.DateField()
    update_user_code = models.ForeignKey(
        "MUser",
        models.DO_NOTHING,
        db_column="update_user_code",
        related_name="m_bank_update_user_code",
    )

    class Meta:
        managed = False
        db_table = "m_bank"


class MChargeType(models.Model):
    charge_type_code = models.IntegerField(primary_key=True)
    charge_type_name = models.CharField(max_length=128, blank=True, null=True)
    regist_user_code = models.IntegerField()
    regist_date = models.DateField()
    update_user_code = models.IntegerField()
    update_date = models.DateField()

    class Meta:
        managed = False
        db_table = "m_charge_type"


class MContractCompany(models.Model):
    company_code = models.IntegerField()
    company_name = models.CharField(max_length=128)
    fixed_cost_code = models.IntegerField(blank=True, null=True)
    regist_user_code = models.IntegerField()
    regist_date = models.DateField()
    update_user_code = models.IntegerField()
    update_date = models.DateField()

    class Meta:
        managed = False
        db_table = "m_contract_company"


class MCreditCard(models.Model):
    credit_card_code = models.IntegerField(primary_key=True)
    credit_card_name = models.CharField(max_length=40)
    regist_date = models.DateField()
    regist_user_code = models.ForeignKey(
        "MUser",
        models.DO_NOTHING,
        db_column="regist_user_code",
        related_name="m_credit_card_regist_user_code",
    )
    update_date = models.DateField()
    update_user_code = models.ForeignKey(
        "MUser",
        models.DO_NOTHING,
        db_column="update_user_code",
        related_name="m_credit_card_update_user_code",
    )

    class Meta:
        managed = False
        db_table = "m_credit_card"


class MEDetailCategory(models.Model):
    e_detail_code = models.IntegerField(primary_key=True)
    e_detail_name = models.CharField(max_length=256)
    regist_user_code = models.IntegerField()
    regist_date = models.DateField()
    update_user_code = models.IntegerField()
    update_date = models.DateField()
    expense_code = models.IntegerField()

    class Meta:
        managed = False
        db_table = "m_e_detail_category"
        unique_together = (("expense_code", "e_detail_code"),)


class MElectronicMoney(models.Model):
    e_money_code = models.IntegerField(primary_key=True)
    e_money_name = models.CharField(max_length=256)
    regist_date = models.DateField()
    regist_user_code = models.IntegerField()
    update_date = models.DateField()
    update_user_code = models.IntegerField()

    class Meta:
        managed = False
        db_table = "m_electronic_money"


class MExpenseCategory(models.Model):
    expense_code = models.IntegerField(primary_key=True)
    expense_name = models.CharField(max_length=40)
    regist_date = models.DateField()
    regist_user_code = models.ForeignKey(
        "MUser",
        models.DO_NOTHING,
        db_column="regist_user_code",
        related_name="m_expense_category_regist_user_code",
    )
    update_date = models.DateField()
    update_user_code = models.ForeignKey(
        "MUser",
        models.DO_NOTHING,
        db_column="update_user_code",
        related_name="m_expense_category_update_user_code",
    )

    class Meta:
        managed = False
        db_table = "m_expense_category"


class MFixedCostItem(models.Model):
    fixed_cost_code = models.IntegerField(primary_key=True)
    fixed_cost_name = models.CharField(max_length=40)
    regist_user_code = models.IntegerField()
    regist_date = models.DateField()
    update_user_code = models.IntegerField()
    update_date = models.DateField()
    expense_code = models.IntegerField(blank=True, null=True)
    payment_cycle_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "m_fixed_cost_item"


class MGiftCertificate(models.Model):
    gift_certificate_code = models.IntegerField(primary_key=True)
    gift_certificate_name = models.CharField(max_length=256)
    regist_user_code = models.IntegerField()
    regist_date = models.DateField()
    update_user_code = models.IntegerField()
    update_date = models.DateField()
    shop_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "m_gift_certificate"


class MMedicalDepartment(models.Model):
    department_code = models.IntegerField(primary_key=True)
    department_name = models.CharField(max_length=256, blank=True, null=True)
    regist_date = models.DateField()
    regist_user_code = models.IntegerField()
    update_date = models.DateField()
    update_user_code = models.IntegerField()

    class Meta:
        managed = False
        db_table = "m_medical_department"


class MMedicalInstitution(models.Model):
    medical_code = models.IntegerField(primary_key=True)
    medical_name = models.CharField(max_length=256, blank=True, null=True)
    regist_date = models.DateField()
    regist_user_code = models.IntegerField()
    update_date = models.DateField()
    update_user_code = models.IntegerField()
    department_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "m_medical_institution"


class MPaymentCycle(models.Model):
    payment_cycle_code = models.IntegerField(primary_key=True)
    payment_cycle_name = models.CharField(max_length=40)
    regist_user_code = models.IntegerField()
    regist_date = models.DateField()
    update_user_code = models.IntegerField()
    update_date = models.DateField()

    class Meta:
        managed = False
        db_table = "m_payment_cycle"


class MPaymentMethod(models.Model):
    payment_code = models.IntegerField(primary_key=True)
    payment_name = models.CharField(max_length=40)
    regist_date = models.DateField()
    regist_user_code = models.ForeignKey(
        "MUser",
        models.DO_NOTHING,
        db_column="regist_user_code",
        related_name="m_payment_method_regist_user_code",
    )
    update_date = models.DateField()
    update_user_code = models.ForeignKey(
        "MUser",
        models.DO_NOTHING,
        db_column="update_user_code",
        related_name="m_payment_method_update_user_code",
    )

    class Meta:
        managed = False
        db_table = "m_payment_method"


class MPoint(models.Model):
    point_code = models.IntegerField(primary_key=True)
    point_name = models.CharField(max_length=256)
    regist_user_code = models.IntegerField()
    regist_date = models.DateField()
    update_user_code = models.IntegerField()
    update_date = models.DateField()

    class Meta:
        managed = False
        db_table = "m_point"


class MQr(models.Model):
    qr_code = models.IntegerField()
    qr_name = models.CharField(max_length=40)
    regist_user_code = models.IntegerField()
    regist_date = models.DateField()
    update_user_code = models.IntegerField()
    update_date = models.DateField()

    class Meta:
        managed = False
        db_table = "m_qr"


class MShop(models.Model):
    shop_code = models.IntegerField(primary_key=True)
    shop_name = models.CharField(max_length=256)
    regist_date = models.DateField()
    regist_user_code = models.ForeignKey(
        "MUser",
        models.DO_NOTHING,
        db_column="regist_user_code",
        related_name="m_shop_regist_user_code",
    )
    update_date = models.DateField()
    update_user_code = models.ForeignKey(
        "MUser",
        models.DO_NOTHING,
        db_column="update_user_code",
        related_name="m_shop_update_user_code",
    )
    shop_name_kana = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "m_shop"


class MTax(models.Model):
    tax_code = models.IntegerField(primary_key=True)
    tax_name = models.CharField(unique=True, max_length=128)
    regist_date = models.DateField()
    regist_user_code = models.IntegerField()
    update_date = models.DateField()
    update_user_code = models.IntegerField()
    payment_cycle_code = models.ForeignKey(
        MPaymentCycle,
        models.DO_NOTHING,
        db_column="payment_cycle_code",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "m_tax"


class TChargeList(models.Model):
    charge_date = models.DateField()
    charge_type_code = models.ForeignKey(
        MChargeType, models.DO_NOTHING, db_column="charge_type_code"
    )
    seq = models.IntegerField()
    amount = models.IntegerField(blank=True, null=True)
    payment_code = models.ForeignKey(
        MPaymentMethod,
        models.DO_NOTHING,
        db_column="payment_code",
        blank=True,
        null=True,
    )
    credit_card_code = models.ForeignKey(
        MCreditCard,
        models.DO_NOTHING,
        db_column="credit_card_code",
        blank=True,
        null=True,
    )
    e_money_code = models.ForeignKey(
        MElectronicMoney,
        models.DO_NOTHING,
        db_column="e_money_code",
        blank=True,
        null=True,
    )
    point_code = models.ForeignKey(
        MPoint, models.DO_NOTHING, db_column="point_code", blank=True, null=True
    )
    gift_certificate_code = models.ForeignKey(
        MGiftCertificate,
        models.DO_NOTHING,
        db_column="gift_certificate_code",
        blank=True,
        null=True,
    )
    regist_user_code = models.IntegerField()
    regist_date = models.DateField()
    update_user_code = models.IntegerField()
    update_date = models.DateField()
    additional_amount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t_charge_list"


class TFixedCostList(models.Model):
    payment_date = models.DateField()
    fixed_cost_code = models.IntegerField()
    payment_code = models.IntegerField()
    credit_card_code = models.IntegerField(blank=True, null=True)
    bank_code = models.CharField(max_length=4, blank=True, null=True)
    usage_start_date = models.DateField()
    usage_end_date = models.DateField(blank=True, null=True)
    company_code = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField()
    regist_user_code = models.IntegerField()
    regist_date = models.DateField()
    update_user_code = models.IntegerField()
    update_date = models.DateField()
    point_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t_fixed_cost_list"


class TMedicalBills(models.Model):
    treatment_date = models.DateField(primary_key=True)
    medical_code = models.ForeignKey(
        MMedicalInstitution, models.DO_NOTHING, db_column="medical_code"
    )
    patient_user_code = models.ForeignKey(
        MUser, models.DO_NOTHING, db_column="patient_user_code"
    )
    burden_amount = models.IntegerField()
    payment_code = models.ForeignKey(
        MPaymentMethod, models.DO_NOTHING, db_column="payment_code"
    )
    regist_date = models.DateField()
    regist_user_code = models.ForeignKey(
        MUser,
        models.DO_NOTHING,
        db_column="regist_user_code",
        related_name="t_medical_bills_regist_user_code",
    )
    update_date = models.DateField()
    update_user_code = models.ForeignKey(
        MUser,
        models.DO_NOTHING,
        db_column="update_user_code",
        related_name="t_medical_bills_update_user_code",
    )

    class Meta:
        managed = False
        db_table = "t_medical_bills"
        unique_together = (
            ("treatment_date", "medical_code", "patient_user_code", "burden_amount"),
        )


class TPaymentBreakdown(models.Model):
    payment_date = models.DateField()
    shop_code = models.IntegerField()
    seq = models.IntegerField()
    amount = models.IntegerField()
    payment_code = models.IntegerField()
    credit_card_code = models.IntegerField(blank=True, null=True)
    e_money_code = models.IntegerField(blank=True, null=True)
    point_code = models.IntegerField(blank=True, null=True)
    gift_certificate_code = models.IntegerField(blank=True, null=True)
    regist_user_code = models.IntegerField()
    regist_date = models.DateField()
    update_user_code = models.IntegerField()
    update_date = models.DateField()
    qr_code = models.IntegerField(blank=True, null=True)
    bank_code = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t_payment_breakdown"
        unique_together = (
            (
                "payment_date",
                "shop_code",
                "seq",
                "payment_code",
                "credit_card_code",
                "e_money_code",
                "point_code",
                "gift_certificate_code",
                "qr_code",
            ),
        )


class TPaymentList(models.Model):
    payment_date = models.DateField(primary_key=True)
    shop_code = models.IntegerField()
    amount = models.IntegerField()
    expense_code = models.IntegerField(blank=True, null=True)
    regist_user_code = models.IntegerField()
    regist_date = models.DateField()
    update_user_code = models.IntegerField()
    update_date = models.DateField()
    e_detail_code = models.IntegerField(blank=True, null=True)
    seq = models.IntegerField()

    class Meta:
        managed = False
        db_table = "t_payment_list"
        unique_together = (("payment_date", "shop_code", "seq"),)


class TTaxPayment(models.Model):
    payment_date = models.DateField(primary_key=True)
    tax_code = models.ForeignKey(MTax, models.DO_NOTHING, db_column="tax_code")
    seq = models.IntegerField()
    amount = models.IntegerField(blank=True, null=True)
    regist_user_code = models.IntegerField()
    regist_date = models.DateField()
    update_user_code = models.IntegerField()
    update_date = models.DateField()
    payment_code = models.IntegerField()
    credit_card_code = models.ForeignKey(
        MCreditCard,
        models.DO_NOTHING,
        db_column="credit_card_code",
        blank=True,
        null=True,
    )
    e_money_code = models.ForeignKey(
        MElectronicMoney,
        models.DO_NOTHING,
        db_column="e_money_code",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "t_tax_payment"
        unique_together = (("payment_date", "tax_code", "seq"),)
