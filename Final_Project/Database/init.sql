-- we don't know how to generate root <with-no-name> (class Root) :(

comment on database postgres is 'default administrative connection database';

create sequence account_id_seq;

alter sequence account_id_seq owner to postgres;

create table account
(
    account_id serial
        primary key,
    balance    double precision,
    payments   double precision,
    purchases  double precision,
    median     double precision
);

alter table account
    owner to postgres;

create table purchase
(
    purchase_id      serial
        primary key,
    account_id       integer
        references account,
    amount           double precision,
    currency         text,
    time             timestamp,
    location         point,
    product_category text,
    result           boolean
);

alter table purchase
    owner to postgres;

create table payment
(
    payment_id serial
        primary key,
    amount     double precision,
    currency   text,
    time       timestamp,
    location   point,
    account_id integer
        references account
);

alter table payment
    owner to postgres;

create table output
(
    output_id      serial
        primary key,
    median_diff    double precision,
    distance_ratio double precision,
    p_id           integer
        references purchase
);

alter table output
    owner to postgres;

create function payment_account_balance() returns trigger
    language plpgsql
as
$$
BEGIN
    UPDATE account
    SET payments = (
        SELECT SUM(amount)
        FROM payment
        WHERE account_id = NEW.account_id
    )
    WHERE account_id = NEW.account_id;

    RETURN NEW;
END;
$$;

alter function payment_account_balance() owner to postgres;

create trigger tr_update_account_balance
    after insert
    on payment
    for each row
execute procedure payment_account_balance();

create function purchase_account_balance() returns trigger
    language plpgsql
as
$$
BEGIN
    UPDATE account
    SET purchases = (
        SELECT SUM(amount)
        FROM purchase
        WHERE account_id = NEW.account_id
    )
    WHERE account_id = NEW.account_id;

    RETURN NEW;
END;
$$;

alter function purchase_account_balance() owner to postgres;

create trigger tr_purchase_account_balance
    after insert
    on payment
    for each row
execute procedure purchase_account_balance();

