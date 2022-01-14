pragma solidity ^0.8.0;

import './TokenFarmUP.sol';

contract TokenFarmV3 is TokenFarmUP {
    function testUpgrade() public view returns(int256){
        return 3;
    } 

    function getUserTotalValueV3(address _user) public view returns(uint256) {
        uint256 totalValue = 0;
        require(uniqueTokensStaked[_user] > 0, "No token staked!");
        for (uint256 allowedTokensIndex = 0; allowedTokensIndex < allowedTokens.length; allowedTokensIndex++) {
            totalValue = totalValue + getUserSingleTokenValue(_user, allowedTokens[allowedTokensIndex]);
        }
        return totalValue;
    }
}