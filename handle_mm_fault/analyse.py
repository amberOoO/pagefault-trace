# %%
# import cudf as pd
import pandas as pd
from pandarallel import pandarallel
import os
import tqdm

pandarallel.initialize()

results_dir = "img"
files = [i for i in os.listdir() if ".log" in i]

for file in tqdm.tqdm(files):

    # %%
    # df = pd.read_csv("llamacpp.llama8b.trace.3conversation_no_cachedrop.log)
    df = pd.read_csv(file)
    df = df.dropna()

    # %%
    df['time'] = df["time"].astype("int")
    df["flags"] = df["flags"].astype("int").parallel_apply(lambda x: f"{bin(x)[2:]}".ljust(10, "0")).astype("str")
    df["retval"] = df["retval"].astype("int").parallel_apply(lambda x: f"{hex(x)}").astype("str")

    # %%
    df["name"].value_counts()

    # %%
    # 过滤掉其他附带的程序
    df = df[df["name"] == "main"]
    df = df.reset_index().drop(columns=["index"])
    
    df = df[df["retval"] != '0x100']

    # %% [markdown]
    # # 虚拟地址转换成pfn

    # %%
    df["pfn"] = df["addr"].apply(lambda x: int(x, 16))
    df["pfn"] = df["pfn"].parallel_apply(lambda x: (x - df["pfn"].min()) // (4 * 1024))
    df["pfn"] = df["pfn"].astype("int")

    # %% [markdown]
    # # Plot

    # %%
    import seaborn as sns
    import matplotlib.pyplot as plt
    import pandas as pd

    # %%
    bin(2)[2:]

    # %%
    plt.figure(figsize=(32,16))
    sns.scatterplot(x=range(len(df)), y=df['pfn'], hue=df["retval"], linewidth=0)
    plt.savefig(f"{results_dir}/{file}.jpg")

    # %%
    kernel_fault = df[df["pfn"] > 3e10]
    user_fault = df[(1e10 < df["pfn"]) & (df["pfn"] <= 3e10)]

    # %%

    plt.figure(figsize=(32,16))
    sns.scatterplot(x=range(len(user_fault)), y=user_fault['pfn'], hue=user_fault["retval"], linewidth=0)
    plt.savefig(f"{results_dir}/{file}-user.jpg")
