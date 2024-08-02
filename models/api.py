import uuid
from datetime import datetime
from enum import Enum, IntEnum
from typing import Optional, List

from pydantic import BaseModel, ValidationError, Field

from models.enum import HttpStatus, BinCode


# ===== Base Models =====
class ErrorData(BaseModel):
    error_code: HttpStatus  # get fastapi status as type
    error_message: str


class MetaData(BaseModel):
    page_size: int = 10
    page: int = 1
    total_page: int = 1


class TraceBase(BaseModel):
    request_id: Optional[str] = Field(title="Client Request ID", alias='request_id',
                                      default_factory=lambda: uuid.uuid4().hex)
    request_date: Optional[datetime] = Field(title="Request Date", alias='request_date',
                                             default_factory=datetime.utcnow)


class TraceInfoBase(TraceBase):
    trace_id: Optional[str] = Field(title="Napas' Trace ID", alias='trace_id', default=None)
    bank_txn_id: Optional[str] = Field(title="Bank's transaction ID", alias='bank_txn_id', default=None)
    bank_date: str = Field(title="Bank Date", alias='bank_date',
                           default=str(datetime.now().timetuple().tm_yday))


class UniCubeBaseResponse(BaseModel):
    trace: Optional[TraceInfoBase] = None
    data: Optional[List[object]] = []
    meta: Optional[MetaData | ErrorData] = None
class ErrorResponse(BaseModel):
    detail: str

class ListBase(BaseModel):
    meta: Optional[MetaData | ErrorData]


class ObjBase(BaseModel):
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    closed_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# ===== API Models =====


class BankAccountBase(BaseModel):
    acc_no: str = Field(title="Bank Account Number", alias='acc_no', default="")
    bincode: BinCode = Field(title="Bank Bin Code", alias='bincode', default=BinCode.OCB)
    acc_holder: str = Field(title="Bank Account Holder", alias='acc_holder', default="")
    acc_status: Optional[bool] = Field(title="Bank Account Status", alias='va_status', default=False)


class VirtualAccountBase(BankAccountBase):
    va_type: bool = Field(title="Virtual Account Type", alias='va_type', default=False)
    va_name: str = Field(title="Virtual Account name", alias='va_name', default="")
    va_no: Optional[str] = Field(title="Virtual Account No", alias='va_no', default=None)
    va_status: Optional[bool] = Field(title="Virtual Account Status", alias='va_status', default=False)
    va_is_verify: Optional[bool] = Field(title="Virtual Account Is Verify", alias='va_is_verify', default=False)


class TransactionBase(BaseModel):
    name: str = Field(title="Transaction Name", alias='name', default="")
    txn_date: datetime = Field(title="Transaction Date", alias='txn_date', default=False)
    txn_type: str = Field(title="Transaction Type", alias='txn_type', default="ibft")
    txn_status: str = Field(title="Transaction Status", alias='txn_status', default="")
    txn_amount: float = Field(title="Transaction Amount", alias='txn_amount', default=0.0)
    txn_fee: float = Field(title="Transaction Fee", alias='txn_fee', default=0.0)
    currency: str = Field(title="Currency", alias='currency', default="")
    narrative: str = Field(title="Narrative", alias='narrative', default="")
    bill_id: str = Field(title="Bill ID", alias='bill_id', default="")
    merchant_id: str = Field(title="Merchant ID", alias='merchant_id', default="")
    merchant_name: str = Field(title="Merchant Name", alias='merchant_name', default="")
    frm_acc_no: str = Field(title="From Account No", alias='frm_acc_no', default="")
    frm_acc_name: str = Field(title="From Acc Name", alias='frm_acc_name', default="")
    frm_acc_bincode: str = Field(title="From Acc Bincode", alias='frm_acc_bincode', default="")
    frm_acc_bankname: str = Field(title="From Acc Bank Name", alias='frm_acc_bankname', default="")
    to_acc_va: str = Field(title="To Acc Va", alias='to_acc_va', default="")
    to_acc_no: str = Field(title="To Acc No", alias='to_acc_no', default="")
    to_acc_name: str = Field(title="To Acc Name", alias='to_acc_name', default="")
    to_acc_bincode: str = Field(title="To Acc Bincode", alias='to_acc_bincode', default="")
    to_acc_bankname: str = Field(title="To Acc Bank name", alias='to_acc_bankname', default="")


# ===== API Models =====
class CreateVirtualAccountRequest(VirtualAccountBase, TraceBase):
    pass


class VirtualAccountResponse(VirtualAccountBase, ObjBase):
    trace: TraceInfoBase = TraceInfoBase()


class VirtualAccountDetailResquest(TraceBase):
    va_no: str = Field(title="Virtual Account No", alias='va_no', default=None)


class VerifyVirtualAccountRequest(VirtualAccountDetailResquest):
    otp_code: str = Field(title="OTP Code", alias='otp_code', default="")


class BankListRequest(TraceBase):
    merchant_id: str = Field(title="Merchant ID", alias='merchant_id', default="")


class BankListResponse(ListBase):
    trace: TraceInfoBase = TraceInfoBase()
    data: Optional[List[BankAccountBase]] = []


class VirtualAccountListRequest(TraceBase):
    acc_no: str = Field(title="Bank Account Number", alias='acc_no', default="")
    bincode: BinCode = Field(title="Bank Bin Code", alias='bincode', default=BinCode.OCB)


class VirtualAccountListResponse(ListBase):
    trace: TraceInfoBase = TraceInfoBase()
    data: Optional[List[VirtualAccountBase]] = []


class TransactionListRequest(TraceBase):
    va_no: str = Field(title="Virtual Account Number", alias='va_no', default="")
    bincode: BinCode = Field(title="Bank Bin Code", alias='bincode', default=BinCode.OCB)


class TransactionListResponse(ListBase):
    trace: TraceInfoBase = TraceInfoBase()
    data: Optional[List[TransactionBase]] = []


class IpnRequest(BaseModel):
    amount: int = Field(title="Amount", alias='amount', default=0)
    currency: str = Field(title="Currency", alias='currency', default="")
    from_acc_no: str = Field(title="Bank Account Number", alias='from_acc_no', default="")
    from_acc_name: str = Field(title="Bank Account name", alias='from_acc_name', default="")
    from_bincode: str = Field(title="Bank Bin Code", alias='from_bincode', default="")
    to_acc_no: str = Field(title="Bank Account Number", alias='from_acc_no', default="")
    to_acc_name: str = Field(title="Bank Account name", alias='from_acc_name', default="")
    to_bincode: str = Field(title="Bank Bin Code", alias='from_bincode', default="")
    narrative: str = Field(title="Narrative", alias='narrative', default="")


class Ipn(TraceBase):
    amount: int = Field(title="Amount", alias='amount', default=0)
    currency: str = Field(title="Currency", alias='currency', default="")
    from_acc_no: str = Field(title="Bank Account Number", alias='from_acc_no', default="")
    from_acc_name: str = Field(title="Bank Account name", alias='from_acc_name', default="")
    from_bincode: str = Field(title="Bank Bin Code", alias='from_bincode', default="")
    to_acc_no: str = Field(title="Bank Account Number", alias='from_acc_no', default="")
    to_acc_name: str = Field(title="Bank Account name", alias='from_acc_name', default="")
    to_bincode: str = Field(title="Bank Bin Code", alias='from_bincode', default="")
    narrative: str = Field(title="Narrative", alias='narrative', default="")


class IpnResponse(ListBase):
    trace: TraceInfoBase = TraceInfoBase()
    data: Ipn
