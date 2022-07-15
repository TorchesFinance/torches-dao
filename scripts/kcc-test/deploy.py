import json
import os

from .. import deployment_config as config
from .. import deploy_dao as dao

from brownie import network

DEPLOYMENTS_JSON = "scripts/" + network.main.show_active() + "/deployments.json"
GAUGE_JSON = "scripts/" + network.main.show_active() + "/gauge.json"

DAO_TOKEN = '0x1e33Fe41fF7373c64FAE3a404435a39Cce42eB0f'
POLICYMAKER_REWARD = 10 ** 18

# name, type weight
GAUGE_TYPES = [
    ("Liquidity", 10 ** 18),
]

# lp token, default point rate, point proportion, reward token, reward rate, gauge weight
POOL_TOKENS = {
    "USDT": ("0xfC49791fF96187ad3260f47CeDdB9c440f25cB6E", 10 ** 16, 10 ** 17, "0x67f6a7BbE0da067A747C6b2bEdF8aBBF7D6f60dc", 10 ** 15, 20),
    "USDC": ("0x3d41B01a94cd8538099005565b38de558CAE5EDA", 10 ** 16, 5 * 10 ** 16, "0xD6c7E27a598714c2226404Eb054e0c074C906Fc9",10 ** 15, 50)
}

def deploy():
    print(DEPLOYMENTS_JSON)
    admin = config.get_live_admin()
    voting_escrow = dao.deploy_part_one(admin, DAO_TOKEN, config.REQUIRED_CONFIRMATIONS, DEPLOYMENTS_JSON)

    dao.deploy_part_two(
        admin, DAO_TOKEN, voting_escrow, POLICYMAKER_REWARD, GAUGE_TYPES, POOL_TOKENS, config.REQUIRED_CONFIRMATIONS, DEPLOYMENTS_JSON
    )

def add_gauge():
    admin = config.get_live_admin()

    with open(GAUGE_JSON) as fp:
        gauge_json = json.load(fp)

    with open(DEPLOYMENTS_JSON) as fp:
        deployments = json.load(fp)

    dao.add_gauge(admin, gauge_json["name"], deployments["Minter"], deployments["RewardPolicyMaker"],
            gauge_json["cToken"], eval(gauge_json["pointRate"]), eval(gauge_json["pointProportion"]),
            gauge_json["rewardToken"], eval(gauge_json["rewardRate"]), gauge_json["weight"],
            config.REQUIRED_CONFIRMATIONS, DEPLOYMENTS_JSON)
