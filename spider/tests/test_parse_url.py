from urllib import parse

base_url = 'https://m.dianping.com/ugc/review/reviewlist?offset=2588&shopUuid=H3lAYNAFcT9F9gR0&optimus_uuid=189b5a8742cc8-1f0e92a62bdd46-0-0-189b5a8742c52&optimus_platform=13&optimus_partner=203&optimus_risk_level=71&optimus_code=10&tagType=1&tag=%E5%85%A8%E9%83%A8&cx=WX__ver1.2.0_CCCC_QZ%2Bjty4uCzVN9G6PMudx0yf1ymr1r7UEqaKRtVdDWv6Y60VJG9iNo56N6%2FBslnnDMzPkRLmWDLwxiTFbh79nLRVET%2Fk0qQS6mMqBua8ngb1bfQn54Zv0zYsRQgcngXrCebeaT%2BSTMVZ%2Fylfz6V4uMYD1j0FPRR4QLWAGGiyh109ET1jfaZT7c6B6H37SFAcfYVoYlf0Cepo9cuZ7NZ057PgltxyU7FYGKgoFtSD%2Bx8YORVbfymOSIBgdVZprZDs%2BC%2B5XSV3mvB%2BZdj90hxgU9r%2FY6X%2F2di8vRlMQ7qjri6CK5nQVFy5jeNkaB6oPq9gpR8Il8RwQcTUzY46mjlul5mGZabT6BXp14ExVwwjJb0cal0DgRQ5IAUYYuUe4Pg6uLGC3b1N78MPAPGDLp7XPKzVbOqEWCqqks%2FyiKhQwq27y5PN4eLVtJSYepyaJvwLy%2B0UnRGxdEmkiZ4kBAHQ4BXGP0ESWTYQW9SyTSv3T830989qLuwM1redyrOiDoW9MvRb3pmVq26mO2rUYv5fDyqnBoyOYmJNMsclMHAzQO1C0KzR0sW0OOSQ29x9roCVVyxwIgELwXvfsvEn%2BV35sGUu%2FGq%2FT5%2BaeisA869mvFFCSq7rblcbJ%2FA8CDJ5%2FlJkn%2BTvoBi%2FqxYmo1TlGTJ43bHd8Atii%2BYBWs%2BoWfpcIdoiAHtNlYTicyGJ18EWc7qTL5qqUZ%2BCyonyORD%2BpZ43CghIGuFVxpI6pzC9nCmZ1TPWPJlrOkwnwVrxBMvoJW%2B7ueRi5qe6rclfzOhuXjWnRs1qCWs4gvvXIgHRE3AzbS%2FLVX4%2FWUtahl9tyuCnECpticbw6nachzhJcPJrs4kgGhUxh1jRBMvbwiuiv61DEZGl7F9CM9XhK79W0gC%2B%2ByW4VPr7%2Fl8x%2BqM6%2F6ChWqs%2Fw%2FiwC0dWFKyNRYI4TXQ%2Bvvmau2gbpWEsqBZqA8bPbZnJALOn1AhMv8HaAPiUeYOczMWocGfFFDuLQM10wzOa23wOOh4mlyhVN8nrOipXtI%2FZTV97TnEA3Y2cMZvHTjDIXhHl2RuAFnovSalK7jnkyXBLJAWzPaEkjmMmex6p3BtsHlHNSCWu5IS%2BFGCTfajr0zfOd5lTrs2puPlqhT7ssWS4c5jAvRu5%2BBXXoBqWLO%2B0jRoLPMNzefVriGOo8bQxUCGNwCDlpj8xKuKxtNMk1j8i2JMlWSsftzVeXE9Ep3f9C9Yox16LWsRX4I7ywJPHQyDMN5tsLFi%2BSDMJYkZl24R7ertRbHxS28pFEce2IUwwrp0UqRBt2UU%2FGAOJ%2FdIle7qYSQq40CbV88Cqs4d7zs3y7CfH59q2HTFovIUOlzAzRxIU9f4AXVBE5aZ5ULWUXKyvLV14NYmcefCCY%2Bx4ZlkL81aBTlfMrQ%2B9yWn2cIso5GM6TbBpsdkNOtN7EkUuABnYdIYWcvUd9oV%2Fb0Wtfq2VmLnJkdVUKJwhfGCGgATZwG4I0dhYm6NOq69MLXAN2mvlvCGGb9cLx%2FDoCPlYzvHTezvMlaae1YMQmkYyGA1r0X5LfQCvxzpMazm%2FwdiQ2Tj2Gevc%2FsHd41%2FkaIVzUUiporT7XH0zRETZ1MsqPwtsuH%2F1a9X5gMIFFtoOGJee1AKC453ed7vS5JzR80JXwS4QPnzGh5xETogW4INuDUrtlEaAG6BbJVI0Vkbb3dHwenxe7DodhuUJMnrSuppUFeqxrS%2BbuXjdJpTHptPWTp0p45gwb2g2R40YTlZJDO99fxjiU%2BixnEh8MgwwMSGtlHm0ALSsiRfelfC9QY8Do3ac%2Bes5F1iwwQ0ZHDzRf3xk25A%3D%3D&mtsiReferrer=%252Fpackages%252Fugc%252Fpages%252Freviewlist%252Freviewlist%253Fmsource%253Dwxappmain%2526shopUuid%253DG7kQ8cIgaZMY58Ma%2526tag%253D%2525E5%252585%2525A8%2525E9%252583%2525A8%2526tagType%253D1&_token=eJxNVdeq7EgS%252FJfzqgtqeem%252BybW8V8st%252ByDvvdew%252F749uwMzUElERiUJRaX542eRsp%252Ffr18%252F2%252FrzG8KpF4VTJI7ACPzrJ%252F2HRmEI%252FqJ%252B%252FSSLx%252F38%252FhcKob8IBP%252F3n4L99f8W%252FmYw%252Bj1%252FRkjfgJ8pTtu4zFdwL1Nw%252Bh9b8qPOz65et3%252FQn18%252F%252F7%252BdxvpP%252B%252Flm6N1vhi%252B2f2H8F25%252F4VqXw8%252Fvn1y%252BsvbJb0IrbbtIb74gsZqppapxcjqDaAs%252BaMDidV21fKJ0Ea3am9ODTxBhxlbwWkjr10MvpEUHHZJazeIgUvIaALFoM2DtgKclH3ojlsonVsLvPzVzzN2EWF7KBDqpPWghu6Aq%252BypgkqJFXbesv%252BctFDg9O9v3EB978YHhcp0KDcPcarFf5Vzuo3cDWrZKfP8iQyLzFbg3HpXhUWUlCyuWij1VRU3bETUUkkeWyOwUo496Kse2VBdHIZ9WMotWYMJ3P85mDSuUFzC89iFIdZckNJNSKwLNskpGXaspKT5Vh4bFM50RR2brm9U0bYJNBwh4Xr08i2DjwaSdMMYxJ3hDeQ9fshO9Uei52BfNwixDuDA%252BWEJN8BADeT0O0beQ03Ttf5Ddm%252Ff4Mp08xi4qTJCJtQv4WT59dHBMr1T3xteTHCOcyyAI1wlkTmRJjXj1m02Np7SaxlSG7LoOIxSdXfLRVyNddZBwqag%252FENtcri1G9ikvjNLGG%252Fu%252B77bkr%252F2A%252BQGpiyCO%252B9In8S7rxEpnA7muxmSol0TKsF3zbnCvApprqSlCo%252BEJIEaMNdN1bbmjdZbLqe9fUuxApPtDoRFt1qwyOVlrvCPiIeQF6quNdDZ4w7g3jIxuOYSElixVwwSZbrp6mm%252BN3C9zuxRzm0CG6OcV5FNcbRHT3p8V9DlMOt8wSOxUWXnl55s8DArlkJNJbOTDXHT10mpTx8dPn%252BJDxIQGLPeyBru%252BY8ldZ1wr4yfDQsNW3jNz%252BhB0EsYfT7QrUNZuc9pinGlNPghNVtUi%252Fx7juJipWHAnKB%252FL2z1k0mlxvXwBtkCLqw7GXiJyjIBL2qa8hpQxyFQObtKPp2E%252FK5jTAQuGuqM5iBObdJt6iTDtq%252Bpiz0k6XIZJ7IMHHSc1bEvpFH5AMTdyGlPxXsiSQF0Bckia9qgMhZeum48mh7CsexadG06zxZcdk10LQ4ONHd5381oAAaJMWWmQfcyqpwX4bmPHd%252B2x8xhYRWfdlkpjsZFrtl46GEFPhlQ%252BXQJsEi36DLl25sDilLJ%252BeCU7aRc%252BwhWZ%252BEsYILKXp2nUGsGZ5Wyyc6raOxkhq8G1d6QfIyKfG6ANa15ClDhUyjPbLrRpXmagEPaykIt7m%252BgDuu9QdpnblKYznzCg4uvZPg43D3Tnw0HJpU%252FjaFOwAWPFpW7HMjJ2pM9gE1UHMiEx5qSAOVVQnkTm4ycUF%252BmrxTDRhDaFhlhBPsbQs5wlCsevD%252FCxbkBNYmmm8AyJNYmWy1GICv4jjmoKKVI8I8FQPYk%252FcrBdDzW6xGWhbrmRmG8wwaET2kKxiCREivcjcQgxDyrifHMkwI5zd%252B4Cn6ZesdCsVxu71cQZlsazsIRrDUmcPgdqaH%252Bb3W8tYIGS2xRgXqQ%252FwGOLshliWKU%252FctglfPYRbKj%252FnC01pz2vJsOblVz3diIlfT9hReTeyfvPecWtkjcNt7bzjugIlEyA7TCfUfyWYZOGDlbvpLDAW2AyjXfWhM5ioV7ahg63YYVG1QW3SuaGLA4ymDz5AW0zHsL3Ubq2ieuhSCkgedO7hDbpjJk9ecOUlCaJ5Cav7tK9v92%252FUtT9ybxaucJXi71qpeQjLwjRaATQyJkZ1REycSdWXAk%252FSneX20MLPYQWrzhBiCO%252BBt6o8CXSc757HbTGRJXTGxeAzFqMXBAaqb5sCBT%252FmOknkNGIHb9rRuwRnEoajdt4UrL3Gklr%252F%252F3qUagOCGtgNdsrJ2eUz2YZx%252BkZNBOqP%252FltR6S9h6C8tRGdilw0C8dr876zxXiZ04gpcJrj5DZcWv3U7i2jfP6BHVNVh7bIBndgOK%252BH98WMnyOEGwVwXSPbaPLoy9498QfhoULIebuylua0Jt7a39ac6xGPD7Mhk9CNWcMDFa0%252FYaIybssOPyXcvIN%252BXm59Z6f0tjApEgdaxcqyOwv77N8cjMH3mEeoXlJmgXgE9HWwCfDFLsdeBQIywYYQMXkrBYY8ADjyUoidcBq1xwBs%252FjSQHdiaT3BB2xE%252FIHsClY9Gm3toBQegKIqIK7osYJkzqh4%252Bu9fnxcaXL3nqlMi%252BJ%252BkTz2Sc49fuDyRtMrlxuvcbYOSBrChrLQrAOCIShcBJEQ40rn1ThQTUB64Z2vZcHA90R4NCOQwvFwxzTcD%252BIMAC6IML2AgEBFCSAsFCHCAKuL9vOcAzzu7ULH7%252B81%252BGDQ8B&isNeedNewReview=1&pullDown=true&reLoad=false&device_system=WINDOWS&wxmp_version=9.37.4'
url = parse.urlparse(base_url)
query = parse.parse_qs(url.query)
del query['tagType']
del query['tag']
del query['isNeedNewReview']
query['offset'] =['{offset}']
query['shopUuid'] = ['{shopUuid}']
l = []
for k,v in query.items():
    l.append(k + '=' + v[0])
qs='&'.join(l)
new_url = parse.urlunparse((url[0],url[1],url[2],url[3], qs ,url[5]))

print(f">> url: {url}")
