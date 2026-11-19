import regex
import snowballstemmer

stem = snowballstemmer.stemmer("english")

stop = [
    "a", "an", "the", "and", "or", "but", "if", "of", "to", "in", "on", "for",
    "with", "at", "by", "from", "is", "are", "was", "were", "be", "been", "am",
    "as", "it", "this", "that", "these", "those", "he", "she", "they", "we",
    "you", "i", "me", "my", "your", "his", "her", "our", "their", "not", "no",
    "do", "does", "did", "have", "has", "had", "so", "than", "then", "there",
    "what", "which", "who", "whom", "when", "where", "why", "how",
]

pat = regex.compile(r"[A-Za-z](?:\.[A-Za-z])+\.?|[A-Za-z]+(?:-[A-Za-z]+)+|[A-Za-z]+(?:['’]s)?")

text1 = "Friends, Romans, countrymen, lend me your ears;"
text2 = "John's new U.S.A. laptop is a state-of-the-art device. The price is high, but the quality is amazing!"
text3 = "The authorization for this authorized project is pending. He authorizes the payments regularly."

gold1 = ["friend", "roman", "countrymen", "lend", "ear"]
gold2 = ["john", "new", "usa", "laptop", "state-of-the-art", "devic", "price", "high", "qualiti", "amaz"]
gold3 = ["author", "author", "project", "pend", "author", "payment", "regular"]


def prepare(text):
    words = []
    for m in pat.finditer(text):
        w = m.group()
        if w.endswith("'s") or w.endswith("’s"):
            w = w[:-2]
        words.append(w)

    low = []
    for w in words:
        if "." in w:
            w = w.replace(".", "")
        low.append(w.lower())

    kept = []
    for w in low:
        if w not in stop:
            kept.append(w)

    roots = []
    for w in kept:
        if w.isalpha():
            roots.append(stem.stemWord(w))
        else:
            roots.append(w)

    return words, low, kept, roots


def find_gold(text):
    t = " ".join(text.split())
    if t == " ".join(text1.split()):
        return gold1
    if t == " ".join(text2.split()):
        return gold2
    if t == " ".join(text3.split()):
        return gold3
    return None


def show(name, text):
    words, low, kept, roots = prepare(text)
    print()
    print(name)
    print(text)
    print("کلمه ها:", words)
    print("کوچک:", low)
    print("بدون کلمه ایست:", kept)
    print("ریشه ها:", roots)

    gold = find_gold(text)
    if gold == None:
        print("برای این جمله لیست آماده نداریم")
        return

    program_words = set(roots)
    gold_words = set(gold)
    both = program_words.intersection(gold_words)

    only_program = []
    for w in program_words:
        if w not in gold_words:
            only_program.append(w)
    only_program.sort()

    only_gold = []
    for w in gold_words:
        if w not in program_words:
            only_gold.append(w)
    only_gold.sort()

    print("Gold: '", gold)
    if len(program_words) == 0:
        print("Precision : 0")
    else:
        p = len(both) / len(program_words)
        print("Precision : " + str(len(both)) + "/" + str(len(program_words)) + " = " + str(round(p, 2)))

    if len(gold_words) == 0:
        print("Recall : 0")
    else:
        r = len(both) / len(gold_words)
        print("Recall : " + str(len(both)) + "/" + str(len(gold_words)) + " = " + str(round(r, 2)))

    if len(only_program) == 0:
        print("اصطلاحات اضافه: 0")
    else:
        print("اصطلاحات اضافه:", only_program)

    if len(only_gold) == 0:
        print("اصطلاحات جا مانده از گلد: 0")
    else:
        print("اصطلاحات جا مانده از گلد:", only_gold)


print("جمله را بنویس")
print("1 یا 2 یا 3 برای متن نمونه")
print("all برای هر سه متن")
print("q برای خروج")

while True:
    line = input("\n> ")
    line = line.strip()
    if line == "":
        continue
    if line == "q" or line == "Q":
        break
    if line == "all" or line == "ALL":
        show("متن 1", text1)
        show("متن 2", text2)
        show("متن 3", text3)
        continue
    if line == "1":
        show("متن 1", text1)
        continue
    if line == "2":
        show("متن 2", text2)
        continue
    if line == "3":
        show("متن 3", text3)
        continue
    show("جمله شما", line)
