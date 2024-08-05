from enum import Enum


class PaymentRecurringType(Enum):
    cof = "cof"
    subscription = "subscription"
    installment = "installment"
    delayed = "delayed"
    resubmission = "resubmission"
    reauthorization = "reauthorization"
    incremental = "incremental"
    noShow = "noShow"
    newCof = "newCof"
    newSubscription = "newSubscription"
    newInstallment = "newInstallment"
