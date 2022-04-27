//SPDX-License-Identifier:MIT
pragma solidity >=0.6.0 <0.9.0;
// safemath

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public addressToamountFunded;

    address[] public founderArray;

    address public owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function Fund() public payable {
        uint256 mimimumUSD = 50 * 10 * 18;
        require(
            getConversionRate(msg.value) >= mimimumUSD,
            "you need speed more than $50 eth"
        );
        addressToamountFunded[msg.sender] += msg.value;
        founderArray.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
       
    }

    function getConversionRate(uint256 _ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 eth_usd = (_ethAmount * ethPrice) / 1000000000000000000;
        return eth_usd;
    }

    function getEnteranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "you are not woner of this contract");
        _;
    }

    function withdraw() public payable onlyOwner {
        // transfer address type to payable address type
        // require msg.sender = owner
        payable(msg.sender).transfer(address(this).balance);
        addressToamountFunded[msg.sender] = 0;
        for (
            uint256 founderIndex = 0;
            founderIndex < founderArray.length;
            founderIndex++
        ) {
            address funder = founderArray[founderIndex];
            addressToamountFunded[funder] = 0;
        }
        founderArray = new address[](0);
    }
}
