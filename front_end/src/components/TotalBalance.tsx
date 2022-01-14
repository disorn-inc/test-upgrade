import { formatUnits } from "@ethersproject/units";
import { Typography } from "@mui/material";
import { useTotalBalance } from "../hooks/useTotalBalance";
import { useTotalBalanceV2 } from "../hooks/useTotalV2";
import { Token } from "./Main";

interface Props {
    token: Token;
} 

export default function TotalBalance({token}: Props) {
    const balance = useTotalBalance(token.address)
    const b2 = useTotalBalanceV2()
    const formattedBalance: number = balance
    ? parseFloat(formatUnits(balance, 18))
    : 0
    const formattedBalance2: number = b2
    ? parseFloat(formatUnits(b2, 18))
    : 0
    console.log(formattedBalance2)
    return (
        <Typography>{formattedBalance}</Typography>
    )
}