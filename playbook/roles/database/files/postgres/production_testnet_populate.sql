begin;
select currency_insert('BTC', 100);
select currency_insert('LTC', 200);
select currency_insert('USD', 300);

insert into markets(base, counter, limit_min, position) values ('BTC', 'USD', 0.01, 100);
insert into markets(base, counter, limit_min, position) values ('LTC', 'BTC', 0.1, 200);

insert into dw_fees(currency, method, deposit_constant, deposit_linear, withdraw_constant, withdraw_linear) values ('BTC', 'blockchain', 0.000, 0.000, 0.001, 0.000);
insert into dw_fees(currency, method, deposit_constant, deposit_linear, withdraw_constant, withdraw_linear) values ('LTC', 'blockchain', 0.000, 0.000, 0.100, 0.000);
insert into dw_fees(currency, method, deposit_constant, deposit_linear, withdraw_constant, withdraw_linear) values ('USD', 'wire', 0.000, 0.000, 0.000, 0.000);

insert into trade_fees(linear, one_way) values (0.005, true);

insert into withdrawal_limits(currency, limit_min, limit_max) values ('BTC', 0.010, 10 );
insert into withdrawal_limits(currency, limit_min, limit_max) values ('LTC', 0.100, 100);
insert into withdrawal_limits(currency, limit_min, limit_max) values ('USD', 1, 10000);

insert into currencies_crypto(currency) values('BTC');
insert into currencies_crypto(currency) values('LTC');

insert into wallets_crypto(currency, last_block_read, balance_min, balance_warn, balance_target, balance_max) values('BTC', 1, 0, 0, 100 , 1000 );
insert into wallets_crypto(currency, last_block_read, balance_min, balance_warn, balance_target, balance_max) values('LTC', 1, 0, 0, 1000, 10000);

insert into users(id, email) values (0, '');
insert into balances (user_id, currency) select 0, currency from currencies;

commit;
