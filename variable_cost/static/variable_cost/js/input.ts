import '../css/input.scss';
// Top App Bar
import { MDCTopAppBar } from '@material/top-app-bar';
// Buttons
import { MDCRipple } from '@material/ripple';
// Text field
import { MDCTextField } from '@material/textfield';
// flatpickr
import flatpickr from 'flatpickr';
import { Japanese } from 'flatpickr/dist/l10n/ja.js';

const topAppBarElement = document.querySelector('.mdc-top-app-bar');
const topAppBar = new MDCTopAppBar(topAppBarElement as Element);

const buttonRipples = [].map.call(
  document.querySelectorAll('.mdc-button'),
  (el: Element) => new MDCRipple(el)
);

const tfPaymentDate = new MDCTextField(
  document.getElementById('mdc-text-payment-date') as HTMLInputElement
);

const tfAmounts = [].map.call(
  document.querySelectorAll('.mdc-text-amount'),
  (el: Element): MDCTextField => new MDCTextField(el)
) as MDCTextField[];

const tfTotalAmount = new MDCTextField(
  document.getElementById('mdc-text-total-amount') as HTMLInputElement
);

tfPaymentDate.listen('change', (e: Event): void => {
  if ((e.target as HTMLInputElement).value) {
    (document.getElementById(
      'payment-date-clear'
    ) as HTMLElement).classList.remove('hidden');
  } else {
    (document.getElementById(
      'payment-date-clear'
    ) as HTMLElement).classList.add('hidden');
  }
});

flatpickr('#id_payment_date', {
  allowInput: true,
  locale: Japanese,
  maxDate: new Date(),
  onOpen: (
    dates: Date[],
    currentDateString: string,
    self: flatpickr.Instance
  ): void => {
    self.setDate(self.input.value, false);
  },
});

document
  .getElementById('payment-date-clear')
  ?.addEventListener('click', (): void => {
    tfPaymentDate.value = '';
    tfPaymentDate.emit('change', {});
  });

document
  .getElementById('id_expense')
  ?.addEventListener('change', (e: Event): void => {
    (document.getElementById('form-input') as HTMLFormElement).submit();
  });

tfAmounts.forEach((tf: MDCTextField): void => {
  tf.listen('change', (): void => {
    let amount = 0;

    tfAmounts.forEach((_tf: MDCTextField): void => {
      if (_tf.value) {
        amount += Number.parseInt(_tf.value, 10);
      }
    });

    tfTotalAmount.value = amount ? amount.toString() : '';
  });
});

Array.from(document.getElementsByClassName('sel-payment-method')).forEach(
  (el: Element): void => {
    el.addEventListener('change', (): void => {
      (document.getElementById('form-input') as HTMLFormElement).submit();
    });
  }
);

Array.from(document.getElementsByClassName('btn-payment-add')).forEach(
  (el: Element): void => {
    el.addEventListener('click', (e: Event): void => {
      (e.currentTarget as HTMLButtonElement).classList.add('hidden');
      document
        .getElementById(
          'payment-row-' +
            (Number.parseInt(
              (e.currentTarget as HTMLButtonElement).dataset['idx'] as string,
              10
            ) +
              1)
        )
        ?.classList.remove('hidden');
    });
  }
);
