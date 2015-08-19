select to_user_id, currency, sum(amount) from transactions group by currency, to_user_id order by currency, sum desc;

select from_user_id, currency, sum(amount) from transactions group by currency, from_user_id order by currency, sum desc;

select user_id, currency, (select coalesce(sum(amount),0.00000000) as assets from transactions t where t.currency = b.currency and to_user_id = b.user_id) - (select coalesce(sum(amount),0.00000000) as liabilities from transactions t where t.currency = b.currency and from_user_id = b.user_id) as expected_balance, b.balance from balances b order by currency, expected_balance desc;

select user_id, currency, balance as reported_balance from balances order by currency, balance desc;

select currency, sum(balance) as liabilities from balances where user_id <> 0 group by currency order by currency, liabilities desc;

select currency, balance as fees_collected from balances where user_id = 0 order by currency, fees_collected desc;

select count(*) as registered_users from users;

select base, counter, count(*) as completed_trades from orders where closed = true group by base, counter;

select base, counter, sum(original - remains) as volume_total_in_base from orders where closed = true group by base, counter;

