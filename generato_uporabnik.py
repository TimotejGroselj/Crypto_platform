import sqlite3 as sql

conn = sql.connect('cryptodata.sqlite')

with conn:
    cur = conn.cursor()
    querry = r"""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
	user_id integer PRIMARY KEY,
	username VARCHAR(50),
	email VARCHAR(50) UNIQUE,
	password VARCHAR(50)
    );
    insert into users (username, email, password) values ('Elsey', 'ecogle0@so-net.ne.jp', '$2a$04$ld/SYENXEd9QaHzuuxFBz.1R4F2mNx8KNg9MN3jcNpgWs/8QTckfm');
    insert into users (username, email, password) values ('Adelheid', 'apenhale1@friendfeed.com', '$2a$04$xsENv2PrAB66bDcok.z5pO1WOUrTmMjC2sEtlMK5i35QOoCLd5Ehu');
    insert into users (username, email, password) values ('Druci', 'draubenheimers2@oaic.gov.au', '$2a$04$mnbDnMRJCY18InFNVmJ2..iB07he.IGQ4UFyS44GfoGMXCqylEvgG');
    insert into users (username, email, password) values ('Fowler', 'fcorten3@google.ru', '$2a$04$PaGXF/uPAtaHmVI5U7kILOZBvdnGNMYHEsNgvIJnA6ZSl9CqyfuJa');
    insert into users (username, email, password) values ('Fidole', 'fyushin4@alexa.com', '$2a$04$kQcseGD5J/Sa4dlzKCdDYeD9P3KuASQOGO7zjC3hjp6suOOuiMSNy');
    insert into users (username, email, password) values ('Minne', 'maveries5@europa.eu', '$2a$04$vfVfd.F8vZU.BdZb9J3wSumOFkLFQrR3drer.p49MQq1fKvqBz.p.');
    insert into users (username, email, password) values ('Dwayne', 'dkettlesting6@nps.gov', '$2a$04$VtV9imo0qI74wyC1L5F/1OfXPVJBP46G4S6VRCZDzagxCsXDdnA7G');
    insert into users (username, email, password) values ('Iggy', 'ilowne7@blogger.com', '$2a$04$mVn.2bcF7TlrReDNf6IabeloP1qY0QT0mX1/EoRdm4L8xgifk2id6');
    insert into users (username, email, password) values ('Bax', 'bpilsworth8@purevolume.com', '$2a$04$.dpBWZ5FCcfkrlwZgm7wTeERtxGHupAltGkyRqLoS7o70AE9kaSxC');
    insert into users (username, email, password) values ('Rik', 'rrudgard9@alexa.com', '$2a$04$eSlNgPPfDg36iBA3Oq6eMu8FAxyJ5Lf4/Quk9OWGf23yeIOjbC4X2');
    insert into users (username, email, password) values ('Gordie', 'gclemitsa@google.ru', '$2a$04$9B30L.rRceW.XEA//r8GUuC4EbEgQ01cWSEnWho9.WyBgaj/.13f6');
    insert into users (username, email, password) values ('Heath', 'hdowntonb@yale.edu', '$2a$04$tK7pSYmm2anoFVc6JZVuqOTmyzC2Nh1MiermROCpFJ/wBiCDo7882');
    insert into users (username, email, password) values ('Dredi', 'dmccarrickc@cargocollective.com', '$2a$04$Avbw/o4ja4sQqWrzghIuruVq58FDuPCb.x.rDAozyFPcLunILckHS');
    insert into users (username, email, password) values ('Archambault', 'ahurld@linkedin.com', '$2a$04$9B5wEGVY8giOMLkZzcefNOW8IWSZs4KR7XcprjMgKatE9djLnn57u');
    insert into users (username, email, password) values ('Merrill', 'mmerrifielde@e-recht24.de', '$2a$04$aBnTI4TRvv4kOKjB.pPcieX8sYd.BCXpHNecMhkSGU/b.gjO6YC7q');
    insert into users (username, email, password) values ('Teodoro', 'tlenaghenf@wisc.edu', '$2a$04$1RR6RJLs/mJfVozYmt47qO5gGar0w9SBLRSWmKGRnmemmLViHPwz2');
    insert into users (username, email, password) values ('Gordon', 'ghogginsg@shareasale.com', '$2a$04$xzsMEmIW2KZzhjKZOmFRiu9qNATxltbHKbSBrlgn1Cl2Ya4lkTrkK');
    insert into users (username, email, password) values ('Hedwig', 'hyurkinh@state.tx.us', '$2a$04$gnuMU10Vtvfj8HLSc9MEj.0tOnVefWSy3rr806BtUOo7KPipcgCPq');
    insert into users (username, email, password) values ('Giulio', 'gcordeni@odnoklassniki.ru', '$2a$04$jbT0EPKkz3zGgrF7kLpD6u0GiHzyjdqEVqhHbaPyI6qGRHNkgxbBG');
    insert into users (username, email, password) values ('Vinnie', 'vgudgenj@wikispaces.com', '$2a$04$5IPeN3jxr3zNjC0sJxpfxuR14pjyVMK/37SMK7QlSHo.w8Ef4f2Ci');
    insert into users (username, email, password) values ('Darill', 'dscholtzk@vimeo.com', '$2a$04$ZhAztO9kIfVBctAon6PZVuNkPT5/RJXFUM0A6X.TWzWaXuZJHv4su');
    insert into users (username, email, password) values ('Irving', 'ifrainl@indiegogo.com', '$2a$04$3w.PRsBZ4zvvyjWaqueXgO/9RNYXbYKH0A3YAfR0qVpPI1ryD9rIK');
    insert into users (username, email, password) values ('Beryle', 'bfantonm@telegraph.co.uk', '$2a$04$tkV15.g8MeBapKLHxmfoKu6GIWn/jZitGM8XaCS6eTmZaLabD6DkK');
    insert into users (username, email, password) values ('Karalee', 'ksextin@statcounter.com', '$2a$04$9GlQc/HGnV4OgPRTHyKK5eTHdgtY1Xh/gdR7ZwNLTI6VZHP0CTV.S');
    insert into users (username, email, password) values ('Ermanno', 'eholywello@devhub.com', '$2a$04$6Rck39tIXLuWRSlA6Yf2CekFuluHI.vURPUTufY6Iz4kVzCoJoJGS');
    insert into users (username, email, password) values ('Nellie', 'nkildalep@google.com.hk', '$2a$04$mlggnXj8J09MPyy5KXsQE.3UHlVIqDOVsl7XS2o3OQh37J61RloIC');
    insert into users (username, email, password) values ('Mechelle', 'mharuardq@baidu.com', '$2a$04$ALBFwKZf6GRRJNLXO/4sf.SZYFqMGS6tqBAn5RzMrC6f.xKouuUmS');
    insert into users (username, email, password) values ('Rosabel', 'rgeertzr@sfgate.com', '$2a$04$QIEACMjIu13MZBfTW5iiPODyN7zdvp/DByhSyiNVONN9IJGVR/4DC');
    insert into users (username, email, password) values ('Kym', 'klorents@weather.com', '$2a$04$/tXRPpg1fZXi75Jy8o7uOenjheAx5SXUnaqCZxsijAxvh4OKAfhJ2');
    insert into users (username, email, password) values ('Eugen', 'edigweedt@discovery.com', '$2a$04$wv/06toFjupLFiIPhA2EAOY7pDFTX//TkQp6yyIRbbDDs06QtErUy');
    insert into users (username, email, password) values ('Sari', 'ssperringu@techcrunch.com', '$2a$04$5oOrhK8YF5FsdSRJnIc/S.fLYVy2DLYTwRBx0.27bwKTzPhjgrxRi');
    insert into users (username, email, password) values ('Agatha', 'apenvardenv@amazon.de', '$2a$04$DrCf54zffV4Sg8gMmkXCK.m8Py1/MhQfJ/7qC14Z68ur19MPczfLS');
    insert into users (username, email, password) values ('Alexandre', 'astedallw@surveymonkey.com', '$2a$04$2I8f5TXR8SzVnEnkucCxCO21yJCBqL89kTAUKfqhzFKHZY0vqACYi');
    insert into users (username, email, password) values ('Nelly', 'narltx@netlog.com', '$2a$04$CNIEXePLG5d2GxHY06EBtetfU3dmkljSuOc3o87HzFWJ1OVF710fC');
    insert into users (username, email, password) values ('Chip', 'cleithharveyy@unicef.org', '$2a$04$nthi9kFERqD6.Vg1iTGOeuaYVs4yTg7dzStZXFG3MP4hVpTncuAky');
    insert into users (username, email, password) values ('Clary', 'cboydellz@google.de', '$2a$04$dwQiF6WO.3/fqx/htB76wuRnMQjm2D7taHMfGPA8ZXtMJgj./rdiS');
    insert into users (username, email, password) values ('Melesa', 'mgiraths10@freewebs.com', '$2a$04$7nSbE88DMXHpadeZbMEsV.9yRFSgxClEgIRAVPQgB44E.5qgxO7Cq');
    insert into users (username, email, password) values ('Ameline', 'aweine11@livejournal.com', '$2a$04$ESAzAUf83vCK/Ym7yLeevOcXjEXsdBzJ492z1RcVeiOCkA6Ii3.0y');
    insert into users (username, email, password) values ('Kelcey', 'kgeorgot12@whitehouse.gov', '$2a$04$iWroGrrzS.k0ImI3Kf.X5eEitvBXERs6rsPXrmgm30x1vAsoGr9si');
    insert into users (username, email, password) values ('Royce', 'rdoche13@nyu.edu', '$2a$04$.2c/N3E2kvkmpFPXD.zVqeC5cpKnDzUn/L6Khqhlrq.PO/2.y/Zdi');
    insert into users (username, email, password) values ('Edith', 'eisakovitch14@irs.gov', '$2a$04$kDM3mus6jvglt7Pkq.cdfuR0Cyr7aJgtexHfZ4VDlGTp0BC4NPAXa');
    insert into users (username, email, password) values ('Charlotta', 'cfrany15@globo.com', '$2a$04$D/qjRdKsBH801D/uJig1iefMfv8/Mm4hT1AmW6R3ifK577V00ifAm');
    insert into users (username, email, password) values ('Amble', 'aogriffin16@addtoany.com', '$2a$04$5g.q1gTJgSDaUDAsexWa3ORX9OMTCLKSDFEmnZRfqFAypjMbfq95O');
    insert into users (username, email, password) values ('Harrison', 'htrangmar17@youtube.com', '$2a$04$MtZzQrD0/zj/0.XQnCAtl.eGA.FEcdGQ6LtEO3Md4GOeF1rpZqLkK');
    insert into users (username, email, password) values ('Dwain', 'dadamolli18@netvibes.com', '$2a$04$k/Kj6FSC7GX4Mo1mG2OzwONRwqkKAvb21w5qeWcLLXdp9TuaIMfIe');
    insert into users (username, email, password) values ('Kordula', 'kwalker19@java.com', '$2a$04$D/CYf7wtIUVrrd7z3L9vdePDyz/0rsGXLyG6VLRwRI85YFY3invDW');
    insert into users (username, email, password) values ('Chickie', 'ccaps1a@de.vu', '$2a$04$rqu1jlxjzMqKLgV.l3zscOGEZnJGe0GG2sEkgeaCQbXClwZq27rEG');
    insert into users (username, email, password) values ('Ronna', 'rliptrot1b@163.com', '$2a$04$wsvzH3LLXDoHGT35jHmh5OfGK0xNGOY.DPEZRl0jA/jmGSGCEb4/W');
    insert into users (username, email, password) values ('Inesita', 'ibenzing1c@go.com', '$2a$04$LDN42uxqPE0/.hZLoKpnZO2RJZ7s8TrsgWO.ddRMskWDqeDU9h9Um');
    insert into users (username, email, password) values ('Liva', 'llundberg1d@arstechnica.com', '$2a$04$HvlX7Wi3k7GqkA1Q4X3VfOVcx2NAvG6y864H5MhCsIs75LLTexdFu');
    insert into users (username, email, password) values ('Silvie', 'sbasketter1e@omniture.com', '$2a$04$4dJNEXNS7ik01Oo3CPO4z.8pzfKurGoOkn0y1EbCImyYSOr.F6IWC');
    insert into users (username, email, password) values ('Nicholle', 'nmacneilly1f@alexa.com', '$2a$04$yZg9Pp.r92fGWq8PLVW.a.OyZX2ATcVCfjdYVdFGsGePPNPe9KNVG');
    insert into users (username, email, password) values ('Terry', 'tmattin1g@usa.gov', '$2a$04$/oSceTHdiabQdmbj6Pf9A.jR7fqA4AURzZ5NeNKT/fSAuhS5/4Tma');
    insert into users (username, email, password) values ('Glen', 'glecount1h@engadget.com', '$2a$04$nRu9imcU9MDX.vx0sCd7KuTgXI0BU/6tDMnXT535WoBV7P.to9JdG');
    insert into users (username, email, password) values ('Eustace', 'eduffil1i@goo.ne.jp', '$2a$04$FzcMyfJL7YsCLV9i3z1gYO60xltq7lrzpBoULzHL8jySnPtBDk6yO');
    insert into users (username, email, password) values ('Ignacio', 'iyewdall1j@ted.com', '$2a$04$efzTIeIutWjN1yeOFVGKu.GE3gFJZf2AlFrOBdtv41mZvkK45ztDa');
    insert into users (username, email, password) values ('Tandi', 'twhitwood1k@hc360.com', '$2a$04$BkUbd847nA7BlYLWTKFTVOSmOdgvJ1OdQbRhh/lUoSPD/upz/dZUa');
    insert into users (username, email, password) values ('Marney', 'mlevington1l@china.com.cn', '$2a$04$KhV9Ze1cVx6fIUcRqrz39OA7W9Pjq2RqYwuU2EG2tm3dOuWfjjPhG');
    insert into users (username, email, password) values ('Beniamino', 'bferroni1m@ibm.com', '$2a$04$28aW0mJiDbgWc9edyHv7jed7ge6WRPe3A6n04Fkl/0XaLCjtjrnFi');
    insert into users (username, email, password) values ('Ax', 'afellgett1n@4shared.com', '$2a$04$4wsr5zlkY78OAIqusbgbs.jgMiwtMISG7Vp94n6/CVBm8PzUyKkWe');
    insert into users (username, email, password) values ('Bil', 'babriani1o@4shared.com', '$2a$04$F/OOmmQD8hrn57vqgVDnnucxHTuCoRIbcMIVhsPMGm0l8u.w7vBpS');
    insert into users (username, email, password) values ('Olenka', 'opiscot1p@pinterest.com', '$2a$04$f85USp35zkvEi3y3ymXAtuq3/6XoQKgsHwJHxL1uFe7z81RnWpNxa');
    insert into users (username, email, password) values ('Ninette', 'ndelooze1q@a8.net', '$2a$04$3d8/NwiAOOTBLUo6dIeD7.lxyy2t5zea/vswPwERlbeZYSW2kOZ0q');
    insert into users (username, email, password) values ('Gerhardine', 'gschooling1r@jigsy.com', '$2a$04$YE2wI9Z2dOOAPtDd0FJ0vuGBeDcn.dLXPRhqwv1wzRl2BZNBOa.v.');
    insert into users (username, email, password) values ('Letisha', 'lsanson1s@seattletimes.com', '$2a$04$RrjUlXqDcKpqJgDX8iYiG.TqNH/Sgg3BzvlW1dQEYIq7WqUkFX/2m');
    insert into users (username, email, password) values ('Tony', 'tarnason1t@ebay.com', '$2a$04$NLho2nRz7fzTXwddvydcc.TudHYf9vMsD.Gfez.1/uz85gr9Q27Ly');
    insert into users (username, email, password) values ('Maribeth', 'mgriggs1u@forbes.com', '$2a$04$UJ5IQ48QS6ylekY6gtX8NuDaE4Kyv6ExiJC7yvuT7MrJTL5XWtVpS');
    insert into users (username, email, password) values ('Bernardina', 'bremer1v@ycombinator.com', '$2a$04$rFroh0gLSpxJkuSWgKbE2eLbRMMlAPmZ3E7tg66A9KgJbfRp/Zm1m');
    insert into users (username, email, password) values ('Michal', 'mmcgowing1w@slideshare.net', '$2a$04$BhMcYC23FpY.bai8YCLCG.pqwUgqsb97ZTfkOAASMcmL8/4K4k9GK');
    insert into users (username, email, password) values ('Lorine', 'lexroll1x@simplemachines.org', '$2a$04$.oRLCkWriNvU313ck2LxT.RZpOw4aSXl257QveVWJIekSI2YBJnH2');
    insert into users (username, email, password) values ('Yankee', 'ywaulker1y@macromedia.com', '$2a$04$MDMnofxyKQT6kP943wFQWO.b2LUJVyH.LqFEc/56WaX9Kxk/Bw4r2');
    insert into users (username, email, password) values ('Keven', 'krichmond1z@archive.org', '$2a$04$.1HNNJEubZ010Y171hd9mu9j6urqzW1wW355JwH6Qga2CG2BmAiKa');
    insert into users (username, email, password) values ('Tarah', 'tpanner20@techcrunch.com', '$2a$04$gXjuMX5BW9K0OMrQrG/2/O08VGJjV4oonZR0X9qRuaiBDXfGcIpFy');
    insert into users (username, email, password) values ('Nady', 'nhourston21@arizona.edu', '$2a$04$loDRMIl76l5OKICoXlK1iuefA0rSn.RrR2Rwzh8V3cyQPghsxyOvO');
    insert into users (username, email, password) values ('Margaux', 'mlethieulier22@arizona.edu', '$2a$04$dTafTOdw0UKkYWfhc9gsheTFsjGA0iZJXANm8BcItt7uLA7Q.k0Ga');
    insert into users (username, email, password) values ('Ladonna', 'lcoal23@berkeley.edu', '$2a$04$5Ktb4oGcKM0piBuwYRsKWeEnTSI.fEkmm1Z7JRrmeKz8Jg3nm3pKO');
    insert into users (username, email, password) values ('Dalton', 'dgrzesiak24@prweb.com', '$2a$04$7pTlnDIcbkxISn1yGzuYu.iWJt4mzGNiNtW1De1SXUftyy7CYBonm');
    insert into users (username, email, password) values ('Xerxes', 'xmaccahey25@webmd.com', '$2a$04$efzo3Ql08zBSwn0joLMQFOO4p9Gc.BxDTfwdz93sEWP3ZLrm7lsHu');
    insert into users (username, email, password) values ('Alick', 'agritsaev26@nifty.com', '$2a$04$JM9sFXzBpBvUfzWX.MxteOOlqYuZiVfcLjc91YW/ymp5n3enRme/2');
    insert into users (username, email, password) values ('Kennan', 'kputt27@sourceforge.net', '$2a$04$lRflW2ypsishzpaE6nBAy.kgV7IvV2OET2mEwHSoNoXHG9oASthxm');
    insert into users (username, email, password) values ('Adelheid', 'ababington28@oracle.com', '$2a$04$Z12L/Yq6FAKbZ/QsYoqFueXZKcVxzRiRbjld958HlEP.T8t5kh9mK');
    insert into users (username, email, password) values ('Parke', 'ploding29@typepad.com', '$2a$04$Dce9NuUQxQiIQS7g5L920uQr6bKc8/SSYm/iqrvHB4/u4x9knOliC');
    insert into users (username, email, password) values ('Taylor', 'tbuzza2a@marketwatch.com', '$2a$04$bbusIGt3sF09HccwJgLyy.9b5CJJVNlBWW.SatsUOTH2GwWdl.bq6');
    insert into users (username, email, password) values ('Willard', 'wwaddell2b@answers.com', '$2a$04$aUzue2SIUaE8vNZKm1pPOuH6U6OnDohS/mauXsCI5T5VofPkUNx4K');
    insert into users (username, email, password) values ('Wynne', 'wmcvanamy2c@washington.edu', '$2a$04$dEpWv2/2TUUyYjCW386w0.uNOzzAdtXKZjIqVNjKiy.89RsjSz5/G');
    insert into users (username, email, password) values ('Darleen', 'dgherardi2d@jalbum.net', '$2a$04$LuM3Kk/DIj6C7MNaIWElXuTOGL4NUEWcAySAjQuAVn4qWo4pzI.Tm');
    insert into users (username, email, password) values ('Jsandye', 'jduerden2e@csmonitor.com', '$2a$04$GC4wa72IFDVs8.dVUGF8JOlaJzsrS2Kv4HomZ16UBZDn.0wDUxVVe');
    insert into users (username, email, password) values ('Jewell', 'jmeachem2f@stanford.edu', '$2a$04$OEcwo798rSMQsxUIp.5P9.srdwqti17ZU4NV2ij6W5pakU7iYDdbe');
    insert into users (username, email, password) values ('Rustin', 'rpreuvost2g@feedburner.com', '$2a$04$czuh6amRCe9L.OHQXU67AelfuwrgEGrsHwJbuKXprdvZt7E.gCrZa');
    insert into users (username, email, password) values ('Tony', 'tlutwidge2h@nationalgeographic.com', '$2a$04$H/tIP4y6g5E8V24i0Qg4huYmGPdUtu6qaQoKF6pqgFfgzk2LgR.tK');
    insert into users (username, email, password) values ('Joline', 'jbeare2i@blogs.com', '$2a$04$Vu5khLTnRkxIRGTqSyp4KOqRwlMPlbSuAET4aJYjY6YzERjbD0oTm');
    insert into users (username, email, password) values ('Wilmette', 'warckoll2j@de.vu', '$2a$04$1CbiDt4.RkWWGCdFu4xz0eXqz1lY3HO0fqemvjAauMuFkrGDPsug.');
    insert into users (username, email, password) values ('Arly', 'agallegos2k@theglobeandmail.com', '$2a$04$fNww5IV4T7K9uVJJtota3.MXxLOg3/1BQeVTVJ9xgZlHzOqstoncK');
    insert into users (username, email, password) values ('Antonetta', 'acardenosa2l@twitter.com', '$2a$04$kMdsLUPuRMUki/zxLewPyeb4MDjpfi3.rE4EBKjog/TGp2ltdwqZ2');
    insert into users (username, email, password) values ('Hale', 'hgallandre2m@cornell.edu', '$2a$04$jEnYgmUPASMGd9kBFkdbaew3MHvrnIAGknF/f..WjfVVoJol1OcMy');
    insert into users (username, email, password) values ('Conn', 'ccusted2n@addthis.com', '$2a$04$B/C257TfNTsgPoW5spXCkeeOyKBBV/RNB2UYVjibRRq4bQ2EYamT2');
    insert into users (username, email, password) values ('Otho', 'oofinan2o@deviantart.com', '$2a$04$RQZiMzHdhM4tUGbnkd45auhrYVlJk6oG4sT3jANA696Q.2GStd1O2');
    insert into users (username, email, password) values ('Emelita', 'esaiens2p@home.pl', '$2a$04$glrnVm5oXdwA771kVXmppeOIFbCWhCeImCJ/tQMft8QCkkGlbEXMK');
    insert into users (username, email, password) values ('Robbin', 'rhornung2q@bloomberg.com', '$2a$04$g4WTIOGqU9EvfqnDlu66A.F6l359LgFbtIMElrnmKc7ZxZVAhy8.6');
    insert into users (username, email, password) values ('Phil', 'plebrun2r@godaddy.com', '$2a$04$CbvtYeuW6rGTQ7lOzKg0RuY1llGJdbuL4vdfPcIuHCKbXgYcguhH2');
    """
    cur.executescript(querry)
    