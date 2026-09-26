from flask import Flask, render_template_string

app = Flask(__name__)


HTML = """
<!DOCTYPE html>
<html lang="en" dir="ltr">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Payo — Smart Finance</title>

    <style>

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background: #0b0d10;
            color: #f5f5f5;
            font-family: Georgia, "Times New Roman", serif;
        }

        .container {
            width: 92%;
            max-width: 1100px;
            margin: auto;
        }

        header {
            padding: 28px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 30px;
            font-weight: bold;
            letter-spacing: 2px;
        }

        nav a {
            color: #aaa;
            text-decoration: none;
            margin-left: 25px;
            font-family: Arial, sans-serif;
        }

        nav a:hover {
            color: white;
        }

        .hero {
            min-height: 75vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }

        .hero h1 {
            font-size: clamp(55px, 10vw, 110px);
            line-height: 0.95;
            margin-bottom: 25px;
        }

        .gold {
            color: #d4af37;
        }

        .hero p {
            max-width: 650px;
            color: #aaa;
            font-family: Arial, sans-serif;
            font-size: 18px;
            line-height: 1.7;
        }

        .buttons {
            margin-top: 35px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            justify-content: center;
        }

        .btn {
            padding: 15px 25px;
            border-radius: 50px;
            text-decoration: none;
            font-family: Arial, sans-serif;
            font-weight: bold;
            transition: 0.2s;
        }

        .primary {
            background: #d4af37;
            color: #080808;
        }

        .secondary {
            border: 1px solid #444;
            color: white;
        }

        .btn:hover {
            transform: translateY(-3px);
        }

        section {
            padding: 90px 0;
        }

        .section-title {
            font-size: 45px;
            margin-bottom: 45px;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }

        .card {
            background: #12161b;
            border: 1px solid #242a31;
            border-radius: 20px;
            padding: 30px;
            min-height: 210px;
        }

        .card-icon {
            font-size: 35px;
            margin-bottom: 20px;
        }

        .card h3 {
            font-size: 25px;
            margin-bottom: 15px;
        }

        .card p {
            color: #999;
            font-family: Arial, sans-serif;
            line-height: 1.7;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }

        .stat {
            padding: 35px;
            border-left: 1px solid #333;
        }

        .stat strong {
            display: block;
            font-size: 45px;
            color: #d4af37;
        }

        .stat span {
            color: #888;
            font-family: Arial, sans-serif;
        }

        .cta {
            text-align: center;
            background: #11151a;
            border: 1px solid #272d34;
            border-radius: 30px;
            padding: 70px 25px;
        }

        .cta h2 {
            font-size: 50px;
            margin-bottom: 20px;
        }

        .cta p {
            color: #999;
            font-family: Arial, sans-serif;
            margin-bottom: 30px;
        }

        footer {
            padding: 50px 0;
            border-top: 1px solid #222;
            color: #666;
            font-family: Arial, sans-serif;
            text-align: center;
        }

        @media (max-width: 800px) {

            nav {
                display: none;
            }

            .cards,
            .stats {
                grid-template-columns: 1fr;
            }

            .hero {
                min-height: 65vh;
            }

            .section-title {
                font-size: 36px;
            }

            .cta h2 {
                font-size: 38px;
            }
        }

    </style>
</head>


<body>

<div class="container">

    <header>

        <div class="logo">
            Payo<span class="gold">.</span>
        </div>

        <nav>
            <a href="#features">Features</a>
            <a href="#technology">Technology</a>
            <a href="#contact">Contact</a>
        </nav>

    </header>


    <main>

        <section class="hero">

            <h1>
                Understand<br>
                Your <span class="gold">Money.</span>
            </h1>

            <p>
                Payo is a smart personal finance assistant that helps
                you track spending, understand financial habits,
                monitor goals and make better decisions.
            </p>

            <div class="buttons">

                <a
                    class="btn primary"
                    href="https://t.me/PayoWallerBot"
                    target="_blank"
                >
                    Open Payo
                </a>

                <a
                    class="btn secondary"
                    href="#features"
                >
                    Explore Payo
                </a>

            </div>

        </section>


        <section id="features">

            <h2 class="section-title">
                What Payo does
            </h2>

            <div class="cards">

                <div class="card">

                    <div class="card-icon">
                        💸
                    </div>

                    <h3>
                        Expense Tracking
                    </h3>

                    <p>
                        Record your expenses quickly and
                        understand where your money goes.
                    </p>

                </div>


                <div class="card">

                    <div class="card-icon">
                        📊
                    </div>

                    <h3>
                        Financial Reports
                    </h3>

                    <p>
                        Turn your financial activity into
                        simple and useful reports.
                    </p>

                </div>


                <div class="card">

                    <div class="card-icon">
                        🎯
                    </div>

                    <h3>
                        Financial Goals
                    </h3>

                    <p>
                        Create goals, track progress and
                        stay focused on what matters.
                    </p>

                </div>


                <div class="card">

                    <div class="card-icon">
                        📡
                    </div>

                    <h3>
                        Payo Radar
                    </h3>

                    <p>
                        Detect unusual spending patterns
                        and financial warning signs.
                    </p>

                </div>


                <div class="card">

                    <div class="card-icon">
                        🧠
                    </div>

                    <h3>
                        Payo Memory
                    </h3>

                    <p>
                        Learn from your financial history
                        and discover your spending habits.
                    </p>

                </div>


                <div class="card">

                    <div class="card-icon">
                        🤖
                    </div>

                    <h3>
                        Payo AI
                    </h3>

                    <p>
                        Get smarter guidance and practical
                        financial insights.
                    </p>

                </div>

            </div>

        </section>


        <section id="technology">

            <h2 class="section-title">
                Built for speed.
            </h2>

            <div class="stats">

                <div class="stat">

                    <strong>24/7</strong>

                    <span>
                        Personal finance assistant
                    </span>

                </div>


                <div class="stat">

                    <strong>100%</strong>

                    <span>
                        Focused on your financial habits
                    </span>

                </div>


                <div class="stat">

                    <strong>∞</strong>

                    <span>
                        Room to grow with you
                    </span>

                </div>

            </div>

        </section>


        <section id="contact">

            <div class="cta">

                <h2>
                    Ready to understand your money?
                </h2>

                <p>
                    Start using Payo and take control
                    of your financial decisions.
                </p>

                <a
                    class="btn primary"
                    href="https://t.me/PayoWallerBot"
                    target="_blank"
                >
                    Launch Payo 🚀
                </a>

            </div>

        </section>

    </main>


    <footer>

        Payo Finance © 2026

        <br><br>

        Smart money management.

    </footer>

</div>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )