from django.views import generic
from django.db import connection, transaction

from .forms import InputForm


class InputView(generic.FormView):
    template_name = "variable_cost/input.html"
    form_class = InputForm
    success_url = "/variable_cost/input"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = form_class(**self.get_form_kwargs())

        with connection.cursor() as cur:
            # 店舗取得
            sql = """
                SELECT
                    MS.SHOP_CODE
                    , MS.SHOP_NAME
                FROM
                    M_SHOP MS
                LEFT JOIN
                    (SELECT
                        SHOP_CODE
                        , MAX(UPDATE_DATE) AS UPDATE_DATE
                    FROM
                        T_PAYMENT_LIST
                    GROUP BY
                        SHOP_CODE
                    ORDER BY
                        UPDATE_DATE DESC
                    FETCH FIRST 20 ROWS ONLY) TPL
                ON
                    MS.SHOP_CODE = TPL.SHOP_CODE
                ORDER BY
                    TPL.UPDATE_DATE DESC NULLS LAST
                    , MS.SHOP_NAME ASC
                """

            cur.execute(sql)
            form.fields["shop"].choices = cur.fetchall()

            # 費目取得
            sql = """
                SELECT
                    EXPENSE_CODE
                    , EXPENSE_NAME
                FROM
                    M_EXPENSE_CATEGORY
                ORDER BY
                    EXPENSE_CODE ASC
                """

            cur.execute(sql)
            form.fields["expense"].choices = cur.fetchall()

            # 費目詳細取得
            expense_code = (
                self.request.POST["expense"] if "expense" in self.request.POST else "10"
            )

            sql = """
                SELECT
                    E_DETAIL_CODE
                    , E_DETAIL_NAME
                FROM
                    M_E_DETAIL_CATEGORY
                WHERE
                    EXPENSE_CODE = :expense_code
                ORDER BY
                    E_DETAIL_CODE ASC
                """

            params = {"expense_code": expense_code}

            cur.execute(sql, params)
            form.fields["expense_detail"].choices = cur.fetchall()
            form.fields["expense_detail"].choices.insert(0, (None, ""))

            # 支払方法
            sql = """
                SELECT
                    PAYMENT_CODE
                    , PAYMENT_NAME
                FROM
                    M_PAYMENT_METHOD
                ORDER BY
                    PAYMENT_CODE ASC
                """

            cur.execute(sql)
            payment_method = cur.fetchall()

            for i in range(1, 6):
                idx = str(i)

                form.fields["payment_method_" + idx].choices = payment_method

                # 支払方法詳細
                if "payment_method_" + idx in self.request.POST:
                    if self.request.POST["payment_method_" + idx] == "10":
                        sql = ""
                    elif self.request.POST["payment_method_" + idx] == "20":
                        sql = """
                            SELECT
                                CREDIT_CARD_CODE AS CODE
                                , CREDIT_CARD_NAME AS NAME
                            FROM
                                M_CREDIT_CARD
                            ORDER BY
                                CREDIT_CARD_CODE ASC
                            """
                    elif self.request.POST["payment_method_" + idx] == "30":
                        sql = """
                            SELECT
                                GIFT_CERTIFICATE_CODE AS CODE
                                , GIFT_CERTIFICATE_NAME AS NAME
                            FROM
                                M_GIFT_CERTIFICATE
                            ORDER BY
                                GIFT_CERTIFICATE_CODE ASC
                            """
                    elif self.request.POST["payment_method_" + idx] == "40":
                        sql = """
                            SELECT
                                E_MONEY_CODE AS CODE
                                , E_MONEY_NAME AS NAME
                            FROM
                                M_ELECTRONIC_MONEY
                            ORDER BY
                                E_MONEY_CODE ASC
                            """
                    elif self.request.POST["payment_method_" + idx] == "60":
                        sql = """
                            SELECT
                                POINT_CODE AS CODE
                                , POINT_NAME AS NAME
                            FROM
                                M_POINT
                            ORDER BY
                                POINT_CODE ASC
                            """
                    elif self.request.POST["payment_method_" + idx] == "70":
                        sql = """
                            SELECT
                                BANK_CODE AS CODE
                                , BANK_NAME AS NAME
                            FROM
                                M_BANK
                            ORDER BY
                                BANK_CODE ASC
                            """
                    elif self.request.POST["payment_method_" + idx] == "80":
                        sql = """
                            SELECT
                                QR_CODE AS CODE
                                , QR_NAME AS NAME
                            FROM
                                M_QR
                            ORDER BY
                                QR_CODE ASC
                            """

                    if sql != "":
                        cur.execute(sql)
                        form.fields["payment_detail_" + idx].choices = cur.fetchall()

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def form_valid(self, form):
        if "btn-regist" in self.request.POST:
            sql = ""
            params = {}

            try:
                with transaction.atomic():
                    with connection.cursor() as cur:
                        # T_PAYMENT_BREAKDOWN
                        PAYMENT_COLUMNS = {
                            "20": "CREDIT_CARD_CODE",
                            "30": "GIFT_CERTIFICATE_CODE",
                            "40": "E_MONEY_CODE",
                            "60": "POINT_CODE",
                            "70": "BANK_CODE",
                            "80": "QR_CODE",
                        }

                        # SEQ取得
                        sql = """
                            SELECT
                                NVL(MAX(SEQ), 0) + 1 AS NEW_SEQ
                            FROM
                                T_PAYMENT_LIST
                            WHERE
                                PAYMENT_DATE = :payment_date
                            AND SHOP_CODE = :shop_code
                            """

                        params = {
                            "payment_date": form.cleaned_data["payment_date"].strftime(
                                "%Y/%m/%d"
                            ),
                            "shop_code": form.cleaned_data["shop"],
                        }

                        cur.execute(sql, params)

                        row = cur.fetchone()

                        if row is None:
                            result = False
                            message = "Error: Get SEQ"

                        else:
                            new_seq = row[0]

                            # T_PAYMENT_LIST
                            sql = """
                                INSERT INTO
                                    T_PAYMENT_LIST (
                                        PAYMENT_DATE
                                        , SHOP_CODE
                                        , SEQ
                                        , AMOUNT
                                        , EXPENSE_CODE
                                        , E_DETAIL_CODE
                                        , REGIST_USER_CODE
                                        , UPDATE_USER_CODE
                                    ) VALUES (
                                        :payment_date
                                        , :shop_code
                                        , :seq
                                        , :amount
                                        , :expense_code
                                        , :e_detail_code
                                        , :regist_user_code
                                        , :update_user_code
                                    )
                                """

                            params = {
                                "payment_date": form.cleaned_data[
                                    "payment_date"
                                ].strftime("%Y/%m/%d"),
                                "shop_code": form.cleaned_data["shop"],
                                "seq": new_seq,
                                "amount": form.cleaned_data["total_amount"],
                                "expense_code": form.cleaned_data["expense"],
                                "e_detail_code": form.cleaned_data["expense_detail"],
                                "regist_user_code": form.cleaned_data["user"],
                                "update_user_code": form.cleaned_data["user"],
                            }

                            cur.execute(sql, params)

                            for i in range(1, 6):
                                idx = str(i)
                                payment_method = form.cleaned_data[
                                    "payment_method_" + idx
                                ]
                                amount = form.cleaned_data["amount_" + idx]

                                if (
                                    payment_method == ""
                                    or amount is None
                                    or amount == 0
                                ):
                                    continue

                                if payment_method in PAYMENT_COLUMNS:
                                    payment_detail_sql = [
                                        ", " + PAYMENT_COLUMNS[payment_method],
                                        ", :payment_detail_code",
                                    ]
                                    payment_detail_param = {
                                        "payment_detail_code": form.cleaned_data[
                                            "payment_detail_" + idx
                                        ]
                                    }
                                else:
                                    payment_detail_sql = ["", ""]
                                    payment_detail_param = {}

                                # T_PAYMENT_BREAKDOWN
                                sql = (
                                    """
                                        INSERT INTO T_PAYMENT_BREAKDOWN (
                                            PAYMENT_DATE
                                            , SHOP_CODE
                                            , SEQ
                                            , AMOUNT
                                            , PAYMENT_CODE
                                    """
                                    + payment_detail_sql[0]
                                    + (
                                        """
                                            , REGIST_USER_CODE
                                            , UPDATE_USER_CODE
                                        ) VALUES (
                                            :payment_date
                                            , :shop_code
                                            , :seq
                                            , :amount
                                            , :payment_code
                                        """
                                    )
                                    + payment_detail_sql[1]
                                    + (
                                        """
                                            , :regist_user_code
                                            , :update_user_code
                                        )
                                        """
                                    )
                                )

                                params = {
                                    "payment_date": form.cleaned_data[
                                        "payment_date"
                                    ].strftime("%Y/%m/%d"),
                                    "shop_code": form.cleaned_data["shop"],
                                    "seq": new_seq,
                                    "amount": amount,
                                    "payment_code": payment_method,
                                    "regist_user_code": form.cleaned_data["user"],
                                    "update_user_code": form.cleaned_data["user"],
                                }
                                params.update(payment_detail_param)

                                cur.execute(sql, params)

                            sql = """
                                SELECT
                                    DISTINCT
                                    TO_CHAR(TPL.PAYMENT_DATE, 'YYYY/MM/DD') AS PAYMENT_DATE
                                    , MS.SHOP_NAME
                                    , TPL.AMOUNT
                                    , TO_CHAR(TPL.REGIST_DATE, 'YYYY/MM/DD HH24:MI:SS') AS REGIST_DATE
                                FROM
                                    T_PAYMENT_LIST TPL
                                INNER JOIN
                                    T_PAYMENT_BREAKDOWN TPB
                                ON
                                    TPL.PAYMENT_DATE = TPB.PAYMENT_DATE
                                AND TPL.SHOP_CODE = TPB.SHOP_CODE
                                AND TPL.SEQ = TPB.SEQ
                                INNER JOIN
                                    M_SHOP MS
                                ON
                                    TPL.SHOP_CODE = MS.SHOP_CODE
                                WHERE
                                    TPL.PAYMENT_DATE = :payment_date
                                AND TPL.SHOP_CODE = :shop_code
                                AND TPL.SEQ = :seq
                                """

                            params = {
                                "payment_date": form.cleaned_data[
                                    "payment_date"
                                ].strftime("%Y/%m/%d"),
                                "shop_code": form.cleaned_data["shop"],
                                "seq": new_seq,
                            }

                            cur.execute(sql, params)

                            row = cur.fetchone()

                            if row is None:
                                raise Exception("Error: Did not regist")

                            else:
                                data = {
                                    "payment_date": row[0],
                                    "shop_name": row[1],
                                    "amount": row[2],
                                    "regist_date": row[3],
                                }

            except Exception as e:
                print(sql, params)
                print("exception error:", e)

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ListView(generic.base.TemplateView):
    template_name = "variable_cost/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        with connection.cursor() as cur:
            sql = """
                SELECT
                    TPL.PAYMENT_DATE
                    , MS.SHOP_NAME
                    , TPL.AMOUNT
                FROM
                    T_PAYMENT_LIST TPL
                LEFT JOIN
                    M_SHOP MS
                ON
                    TPL.SHOP_CODE = MS.SHOP_CODE
                ORDER BY
                    PAYMENT_DATE DESC
                """

            cur.execute(sql)

            columns = [col[0].lower() for col in cur.description]
            context["cost_list"] = [dict(zip(columns, row)) for row in cur.fetchall()]

        return context
