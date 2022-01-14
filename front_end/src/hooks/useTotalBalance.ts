import { useContractCall, useContractFunction, useEthers, useTokenBalance } from "@usedapp/core";
import TokenFarmUp from "../chain-info/contracts/TokenFarmV3.json";
import networkMapping from "../chain-info/deployments/map.json";
import { constants } from "ethers";
import { utils, BigNumber } from "@usedapp/core/node_modules/ethers";

export const useTotalBalance = (address: string): BigNumber | undefined => {
    const { chainId, account } = useEthers();
    const { abi } = TokenFarmUp;
    const proxyAddress = chainId ? networkMapping[String(chainId)]["TransparentUpgradeableProxy"][0] : constants.AddressZero;
    // console.log(proxyAddress)
    const tokenFarmInterface = new utils.Interface(abi);
    // const tokenFarmContract = new Contract(proxyAddress, tokenFarmInterface);

    // const {send: totalSend, state: totalState} = useContractFunction(
    //     tokenFarmContract, "getConstValue", {transactionName: "Total Balance"}
    // )
    // const total = totalSend().then(res => res)
    // console.log(total)
    // return {total};
    const b = useTokenBalance(address, account);
    const [stakingBalance] =
    useContractCall({
      abi: tokenFarmInterface,
      address: proxyAddress,
      method: "stakingBalance",
      args: [address, account],
    }) ?? []
    console.log(b)
    return stakingBalance;
}