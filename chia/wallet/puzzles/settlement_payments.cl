(mod (coins_paid)
  ;; `coins_paid` is a list of notarized coin payments
  ;; a notarized coin payment is `(nonce puzzle_hash amount ...)`
  ;; Each notarized coin payment creates a `(CREATE_COIN puzzle_hash amount)` payment
  ;; and a `(CREATE_PUZZLE_ANNOUNCEMENT (sha256tree notarized_coin_payment))` announcement
  ;; The idea is the other side of this trade requires observing the announcement from a
  ;; `settlement_payments` puzzle hash as a condition of one or more coin spends.

  (include condition_codes.clvm)

  (defun sha256tree (TREE)
     (if (l TREE)
         (sha256 2 (sha256tree (f TREE)) (sha256tree (r TREE)))
         (sha256 1 TREE)
     )
  )

  (defun-inline create_coin_for_payment (notarized_coin_payment)
    (c CREATE_COIN (r notarized_coin_payment))
  )

  (defun-inline create_announcement_for_payment (notarized_coin_payment)
      (list CREATE_PUZZLE_ANNOUNCEMENT
            (sha256tree notarized_coin_payment))
  )

  (defun-inline augment_condition_list (notarized_coin_payment so_far)
      (c (create_coin_for_payment notarized_coin_payment)
         (c (create_announcement_for_payment notarized_coin_payment) so_far))
  )

  (defun construct_create_coin_list (coins_paid)
    (if coins_paid
        (augment_condition_list (f coins_paid) (construct_create_coin_list (r coins_paid)))
        0
    )
  )

  (construct_create_coin_list coins_paid)
)
