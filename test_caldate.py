import datetime
import pytest
from caldate import DateError, Date, parse_args, diff_dates, shift_date

class TestDate:
    def test_today(self):
        assert Date('today').date() == datetime.date.today()

    def test_m_d_1(self):
        today = datetime.date.today()
        assert Date('4/1').date() == datetime.date(today.year, 4, 1)

    def test_m_d_2(self):
        with pytest.raises(DateError):
            Date('2/0')

    def test_m_d_3(self):
        with pytest.raises(DateError):
            Date('0/1')

    def test_mm_dd_1(self):
        today = datetime.date.today()
        assert Date('12/31').date() == datetime.date(today.year, 12, 31)

    def test_mm_dd_2(self):
        with pytest.raises(DateError):
            Date('2/30')

    def test_mm_dd_3(self):
        with pytest.raises(DateError):
            Date('9/31')

    def test_mm_dd_4(self):
        with pytest.raises(DateError):
            Date('00/01')

    def test_mm_dd_5(self):
        with pytest.raises(DateError):
            Date('05/00')

    def test_m_d_yy_1(self):
        assert Date('4/1/00').date() == datetime.date(2000, 4, 1)

    def test_m_d_yy_2(self):
        assert Date('1/1/70').date() == datetime.date(1970, 1, 1)

    def test_m_d_yy_3(self):
        assert Date('1/1/69').date() == datetime.date(2069, 1, 1)

    def test_mm_dd_yy_1(self):
        assert Date('2/29/20').date() == datetime.date(2020, 2, 29)

    def test_mm_dd_yy_2(self):
        with pytest.raises(DateError):
            Date('2/29/21')

    def test_mm_dd_yy_3(self):
        with pytest.raises(DateError):
            Date('3/41/05')

    def test_mm_dd_yy_4(self):
        with pytest.raises(DateError):
            Date('00/01/05')

    def test_mm_dd_yy_5(self):
        with pytest.raises(DateError):
            Date('12/00/08')

    def test_m_d_yyyy_1(self):
        assert Date('2/3/1985').date() == datetime.date(1985, 2, 3)

    def test_m_d_yyyy_2(self):
        assert Date('2/29/1988').date() == datetime.date(1988, 2, 29)

    def test_m_d_yyyy_3(self):
        with pytest.raises(DateError):
            assert Date('0/3/1985')

    def test_m_d_yyyy_4(self):
        with pytest.raises(DateError):
            assert Date('3/0/1985')

class TestDiffDates:
    def test_same_date_1(self):
        assert diff_dates(Date('today'), Date('today')) == 0

    def test_same_date_2(self):
        assert diff_dates(Date('3/1'), Date('3/1')) == 0

    def test_same_date_3(self):
        assert diff_dates(Date('02/29/1996'), Date('2/29/96')) == 0

    def test_positive_diff_1(self):
        assert diff_dates(Date('3/1'), Date('3/2')) == 1

    def test_positive_diff_2(self):
        assert diff_dates(Date('02/28/1996'), Date('2/29/96')) == 1

    def test_positive_diff_3(self):
        assert diff_dates(Date('02/28/1996'), Date('3/1/96')) == 2

    def test_positive_diff_4(self):
        assert diff_dates(Date('1/1/03'), Date('1/1/2004')) == 365

    def test_positive_diff_5(self):
        assert diff_dates(Date('1/1/04'), Date('1/1/2005')) == 366

    def test_negative_diff_1(self):
        assert diff_dates(Date('3/2'), Date('3/1')) == -1

    def test_negative_diff_2(self):
        assert diff_dates(Date('2/29/96'), Date('02/28/1996')) == -1

    def test_negative_diff_3(self):
        assert diff_dates(Date('3/1/96'), Date('02/28/1996')) == -2

    def test_negative_diff_4(self):
        assert diff_dates(Date('1/1/2004'), Date('1/1/03')) == -365

    def test_negative_diff_5(self):
        assert diff_dates(Date('1/1/2005'), Date('1/1/04')) == -366

class TestShiftDate:
    def test_no_shifts_1(self):
        today = Date('today')
        assert shift_date(today, 0) == today

    def test_no_shifts_2(self):
        today = Date('today')
        assert shift_date(shift_date(today, 39), -39) == today

    def test_no_shifts_3(self):
        today = Date('today')
        assert shift_date(shift_date(today, -88), 88) == today

    def test_positive_shift_1(self):
        today = Date('today')
        assert shift_date(today, 100) == Date(today.date() + datetime.timedelta(days=100))

    def test_positive_shift_2(self):
        assert shift_date(Date('2/28/96'), 1) == Date('2/29/96')

    def test_positive_shift_3(self):
        assert shift_date(Date('1/1/2003'), 365) == Date('1/1/2004')

    def test_positive_shift_5(self):
        assert shift_date(Date('1/1/2004'), 366) == Date('1/1/2005')

    def test_negative_shift_1(self):
        today = Date('today')
        assert shift_date(today, -100) == Date(today.date() + datetime.timedelta(days=-100))

    def test_negative_shift_2(self):
        assert shift_date(Date('2/29/96'), -1) == Date('2/28/96')

    def test_negative_shift_3(self):
        assert shift_date(Date('1/1/2004'), -365) == Date('1/1/2003')

    def test_negative_shift_5(self):
        assert shift_date(Date('1/1/2005'), -366) == Date('1/1/2004')

class TestParseArgs:
    def test_diff_dates_1(self):
        assert parse_args(['1/1/19', '12/31/2000']) == (
            Date('1/1/2019'), Date('12/31/2000'), True)

    def test_diff_dates_2(self):
        assert parse_args(['-q', '1/1/19', '12/31/2000']) == (
            Date('1/1/2019'), Date('12/31/2000'), False)

    def test_diff_dates_3(self):
        assert parse_args(['-q', 'today', '12/31/2000']) == (
            Date('today'), Date('12/31/2000'), False)

    def test_shift_date_1(self):
        assert parse_args(['1/1/19', '25']) == (Date('1/1/2019'), 25, True)

    def test_shift_date_2(self):
        assert parse_args(['-q', '1/1/19', '-25']) == (Date('1/1/2019'), -25, False)

    def test_shift_date_3(self):
        assert parse_args(['-q', 'today', '0']) == (Date('today'), 0, False)

    def test_invalid_option(self):
        with pytest.raises(SystemExit):
            parse_args(['-a', '1/1/19', '12/31/2000'])

    def test_invalid_date_1(self):
        with pytest.raises(SystemExit):
            parse_args(['1/0', '12/31/2000'])

    def test_invalid_date_2(self):
        with pytest.raises(SystemExit):
            parse_args(['12/31/2000', '2/30'])

    def test_invalid_date_3(self):
        with pytest.raises(SystemExit):
            parse_args(['Dec 1', '12/31/2000'])

    def test_invalid_date_4(self):
        with pytest.raises(SystemExit):
            parse_args(['1/', '12/31/2000'])

    def test_invalid_ndays_1(self):
        with pytest.raises(SystemExit):
            parse_args(['1/1', 'abc'])

    def test_invalid_ndays_2(self):
        with pytest.raises(SystemExit):
            parse_args(['1/1', '3.5'])

    def test_not_enough_arguments(self):
        with pytest.raises(SystemExit):
            parse_args(['1/1'])