import requests
from bip_utils import (
    Bip39MnemonicGenerator,
    Bip39SeedGenerator,
    Bip84,
    Bip84Coins,
    Bip44Changes,
    Bip39WordsNum,
)


def bip():
    return Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)

def generate_ltc_wallet_address(mnemonic):
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    bip84_ctx = Bip84.FromSeed(seed_bytes, Bip84Coins.LITECOIN)
    wallet = bip84_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    return mnemonic, wallet.PublicKey().ToAddress()


def check_ltc_balance(address):
    url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("final_balance")
    return None


def main():
    tries=1
    while True:
        mnemonic = bip()
        ltc_address = generate_ltc_wallet_address(mnemonic)
        ltc_balance = check_ltc_balance(ltc_address[1])
        if ltc_balance is not None and ltc_balance > 0:
            print(f"tries: {tries} | mnemonic: {mnemonic} | address: {ltc_address[1]} | balance: {ltc_balance}")
            break
        else:
            print(f"tries: {tries} | mnemonic: {mnemonic} | address: {ltc_address[1]} | balance: {ltc_balance}")
            tries+=1


if __name__ == "__main__":
    main()
        