// SPDX-License-Identifier: GPL-3.0

pragma solidity 0.6.10;

import "./TokenPool.sol";
import "./Ownable.sol";
import "./IERC20.sol";
import "./SafeMath.sol";

contract Faucet{

    using SafeMath for uint256;
    IERC20 public token;
    address private _owner;
    mapping (address => uint256)usersClaim;

    constructor (IERC20 Token) public{
        _owner=msg.sender;
        token = Token;
    }

    function claim() external{
        _claim(msg.sender);
    }

    modifier onlyOwner() {
        require(isOwner(), "Only owner can call");
        _;
    }

    /**
     * @return true if `msg.sender` is the owner of the contract.
     */
    function isOwner() public view returns (bool) {
        return msg.sender == _owner;
    }

    function lock(uint256 amount) external onlyOwner {
        token.transferFrom(msg.sender, address(this), amount);
    }


    function _claim(address user)private{
        if(usersClaim[msg.sender]==0){
            token.transfer(user, 1000);
            usersClaim[msg.sender]=now;
        }
        else if(now > usersClaim[msg.sender]+ 1 days){
            token.transfer(user, 100);
        }
        else{
            token.transfer(user, 1);
        }
    
    }

    //View Functions

    function FaucetAmount()public view returns(uint256){
        return token.balanceOf(address(this));
    }

    function UserTimeStamp()public view returns(uint256){
        return (usersClaim[msg.sender]);
    }

    function UserToClaim()public view returns(uint256){
        return (usersClaim[msg.sender] + 1 days - now);
    }


}
