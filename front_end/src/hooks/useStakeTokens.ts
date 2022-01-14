import { useContractFunction, useEthers } from "@usedapp/core";
import TokenFarmUP from "../chain-info/contracts/TokenFarmV3.json";
import ERC20 from "../chain-info/contracts/MockERC20.json";
import networkMapping from "../chain-info/deployments/map.json";
import { constants } from "ethers";
import { utils } from "@usedapp/core/node_modules/ethers";
import { Contract } from "@ethersproject/contracts"
import { useEffect, useState } from "react";


export const useStakeTokens = (tokenAddress: string) => {
    // approve => address, abi, chainId
    // stake token

    const { chainId } = useEthers();
    const { abi } = TokenFarmUP;
    const proxyAddress = chainId ? networkMapping[String(chainId)]["TransparentUpgradeableProxy"][0] : constants.AddressZero;

    const tokenFarmInterface = new utils.Interface(abi);
    const tokenFarmContract = new Contract(proxyAddress, tokenFarmInterface);

    const erc20ABI = ERC20.abi;
    const erc20Interface = new utils.Interface(erc20ABI);
    const erc20Contract = new Contract(tokenAddress, erc20Interface);

    const {send: approveErc20Send, state: approveAndStakeErc20State} = useContractFunction(
        erc20Contract, "approve", {transactionName: "Approve ERC20 transfer",}
    );

    const approveAndStake = (amount: string) => {
        setAmountToStake(amount);
        return approveErc20Send(proxyAddress, amount);
    }

    const {send: stakeSend, state: stakeState} = useContractFunction(
        tokenFarmContract, "stakeTokens", {transactionName: "Stake Tokens"}
    );


    const [amountToStake, setAmountToStake] = useState("0");

    useEffect(() => {
        if (approveAndStakeErc20State.status === "Success") {
            console.log("amount",amountToStake)
            console.log("tokenFarm",proxyAddress)
            stakeSend(amountToStake, tokenAddress);
        }
    }, [approveAndStakeErc20State, amountToStake, tokenAddress]);

    const [state, setState] = useState(approveAndStakeErc20State);

    useEffect(() => {
        if(approveAndStakeErc20State.status === "Success") {
            setState(stakeState);
        } else {
            setState(approveAndStakeErc20State);
        }
    },[approveAndStakeErc20State, stakeState])

    return {approveAndStake, state};
}