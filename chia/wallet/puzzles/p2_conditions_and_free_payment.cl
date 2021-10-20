(mod (CONDITIONS EXTRA_VALUE settlement_address)
    (include condition_codes.clvm)

    (if settlement_address
        (c (list CREATE_COIN settlement_address EXTRA_VALUE) CONDITIONS)
        CONDITIONS
    )
)
