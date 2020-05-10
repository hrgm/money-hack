from django import forms


class InputForm(forms.Form):
    user = forms.CharField(required=True, widget=forms.HiddenInput, initial="10")
    payment_date = forms.DateField(label="支払日", required=True)
    shop = forms.ChoiceField(label="店名", required=True)
    expense = forms.ChoiceField(label="費目", required=True)
    expense_detail = forms.ChoiceField(label="費目詳細", required=False)
    total_amount = forms.IntegerField(
        label="合計金額", required=True, max_value=5000000, min_value=0
    )
    payment_method_1 = forms.ChoiceField(label="支払方法1", required=False)
    payment_detail_1 = forms.ChoiceField(label="支払方法詳細1", required=False)
    amount_1 = forms.IntegerField(
        label="金額1", required=False, max_value=1000000, min_value=0
    )
    payment_method_2 = forms.ChoiceField(label="支払方法2", required=False)
    payment_detail_2 = forms.ChoiceField(label="支払方法詳細2", required=False)
    amount_2 = forms.IntegerField(
        label="金額2", required=False, max_value=1000000, min_value=0
    )
    payment_method_3 = forms.ChoiceField(label="支払方法3", required=False)
    payment_detail_3 = forms.ChoiceField(label="支払方法詳細3", required=False)
    amount_3 = forms.IntegerField(
        label="金額3", required=False, max_value=1000000, min_value=0
    )
    payment_method_4 = forms.ChoiceField(label="支払方法4", required=False)
    payment_detail_4 = forms.ChoiceField(label="支払方法詳細4", required=False)
    amount_4 = forms.IntegerField(
        label="金額4", required=False, max_value=1000000, min_value=0
    )
    payment_method_5 = forms.ChoiceField(label="支払方法5", required=False)
    payment_detail_5 = forms.ChoiceField(label="支払方法詳細5", required=False)
    amount_5 = forms.IntegerField(
        label="金額5", required=False, max_value=1000000, min_value=0
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["payment_date"].widget.attrs.update(
            {"class": "mdc-text-field__input", "aria-labelledby": "payment-date",}
        )
        self.fields["total_amount"].widget.attrs.update(
            {
                "class": "mdc-text-field__input",
                "aria-labelledby": "total-amount",
                "readonly": True,
            }
        )

        self.fields["payment_method_1"].widget.attrs.update(
            {"class": "sel-payment-method"}
        )
        self.fields["payment_method_2"].widget.attrs.update(
            {"class": "sel-payment-method"}
        )
        self.fields["payment_method_3"].widget.attrs.update(
            {"class": "sel-payment-method"}
        )
        self.fields["payment_method_4"].widget.attrs.update(
            {"class": "sel-payment-method"}
        )
        self.fields["payment_method_5"].widget.attrs.update(
            {"class": "sel-payment-method"}
        )

        self.fields["amount_1"].widget.attrs.update(
            {"class": "mdc-text-field__input", "aria-labelledby": "amount-1"}
        )
        self.fields["amount_2"].widget.attrs.update(
            {"class": "mdc-text-field__input", "aria-labelledby": "amount-2"}
        )
        self.fields["amount_3"].widget.attrs.update(
            {"class": "mdc-text-field__input", "aria-labelledby": "amount-3"}
        )
        self.fields["amount_4"].widget.attrs.update(
            {"class": "mdc-text-field__input", "aria-labelledby": "amount-4"}
        )
        self.fields["amount_5"].widget.attrs.update(
            {"class": "mdc-text-field__input", "aria-labelledby": "amount-5"}
        )
