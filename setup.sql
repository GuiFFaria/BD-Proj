CREATE TABLE pacientes (
	id_pac	 SERIAL,
	username VARCHAR(256) NOT NULL,
	email	 VARCHAR(20) NOT NULL,
	password VARCHAR(20) NOT NULL,
	PRIMARY KEY(id_pac)
);

CREATE TABLE trabalhadores (
	id_trab	 SERIAL,
	username	 VARCHAR(256) NOT NULL,
	email	 VARCHAR(20) NOT NULL,
	password	 VARCHAR(20) NOT NULL,
	dur_contrato INTEGER NOT NULL,
	salary	 INTEGER NOT NULL,
	PRIMARY KEY(id_trab)
);

CREATE TABLE medico (
	licenca		 INTEGER NOT NULL,
	trabalhadores_id_trab INTEGER,
	PRIMARY KEY(trabalhadores_id_trab)
);

CREATE TABLE enfermeiro (
	role			 VARCHAR(20) NOT NULL,
	categoria		 VARCHAR(20) NOT NULL,
	trabalhadores_id_trab INTEGER,
	PRIMARY KEY(trabalhadores_id_trab)
);

CREATE TABLE assistente (
	seccao		 VARCHAR(512),
	trabalhadores_id_trab INTEGER,
	PRIMARY KEY(trabalhadores_id_trab)
);

CREATE TABLE especializacao (
	id_espec	 SERIAL,
	especializacao VARCHAR(512) NOT NULL,
    id_medico INTEGER,
	PRIMARY KEY(id_espec)
);

CREATE TABLE consulta (
	id_cons			 SERIAL,
	hora			 TIMESTAMP NOT NULL,
	data			 DATE NOT NULL,
	fatura_id_fatura		 INTEGER NOT NULL,
	medico_trabalhadores_id_trab INTEGER NOT NULL,
	pacientes_id_pac		 INTEGER NOT NULL,
	PRIMARY KEY(id_cons)
);

CREATE TABLE internamento (
	id_inter			 SERIAL,
	hora				 TIMESTAMP NOT NULL,
	dia				 DATE NOT NULL,
	pacientes_id_pac		 INTEGER NOT NULL,
	fatura_id_fatura		 INTEGER NOT NULL,
	enfermeiro_trabalhadores_id_trab INTEGER NOT NULL,
	PRIMARY KEY(id_inter)
);

CREATE TABLE cirurgia (
	id_cirur			 SERIAL,
	internamento_id_inter	 INTEGER NOT NULL,
	medico_trabalhadores_id_trab INTEGER NOT NULL,
	PRIMARY KEY(id_cirur)
);

CREATE TABLE receita (
	id_receita SERIAL,
	validade	 DATE NOT NULL,
	PRIMARY KEY(id_receita)
);

CREATE TABLE medicamento (
	id_medicamento SERIAL,
	nome		 VARCHAR(20) NOT NULL,
	PRIMARY KEY(id_medicamento)
);

CREATE TABLE efeito_secundario (
	id_efeito SERIAL,
	descricao VARCHAR(256) NOT NULL,
	PRIMARY KEY(id_efeito)
);

CREATE TABLE fatura (
	id_fatura	 SERIAL,
	valor_total BIGINT NOT NULL,
	PRIMARY KEY(id_fatura)
);

CREATE TABLE pagamento (
	id_pagamento	 SERIAL,
	valor_pago	 BIGINT NOT NULL,
	fatura_id_fatura INTEGER NOT NULL,
	PRIMARY KEY(id_pagamento)
);

CREATE TABLE caract_efeit_sec (
	severity			 INTEGER NOT NULL,
	probability		 INTEGER NOT NULL,
	efeito_secundario_id_efeito INTEGER,
	medicamento_id_medicamento	 INTEGER,
	PRIMARY KEY(efeito_secundario_id_efeito,medicamento_id_medicamento)
);

CREATE TABLE dosagem (
	dosagem			 VARCHAR(512),
	medicamento_id_medicamento INTEGER,
	receita_id_receita	 INTEGER,
	PRIMARY KEY(medicamento_id_medicamento,receita_id_receita)
);

CREATE TABLE consulta_enfermeiro (
	consulta_id_cons		 INTEGER,
	enfermeiro_trabalhadores_id_trab INTEGER,
	PRIMARY KEY(consulta_id_cons,enfermeiro_trabalhadores_id_trab)
);

CREATE TABLE receita_consulta (
	receita_id_receita INTEGER,
	consulta_id_cons	 INTEGER NOT NULL,
	PRIMARY KEY(receita_id_receita)
);

CREATE TABLE internamento_receita (
	internamento_id_inter INTEGER NOT NULL,
	receita_id_receita	 INTEGER,
	PRIMARY KEY(receita_id_receita)
);

CREATE TABLE cirurgia_enfermeiro (
	cirurgia_id_cirur		 INTEGER,
	enfermeiro_trabalhadores_id_trab INTEGER,
	PRIMARY KEY(cirurgia_id_cirur,enfermeiro_trabalhadores_id_trab)
);

CREATE TABLE especializacao_especializacao (
	especializacao_id_espec	 INTEGER,
	especializacao_id_espec1 INTEGER NOT NULL,
	PRIMARY KEY(especializacao_id_espec)
);


ALTER TABLE pacientes ADD UNIQUE (username, email, password);
ALTER TABLE trabalhadores ADD UNIQUE (username, email, password);
ALTER TABLE medico ADD CONSTRAINT medico_fk1 FOREIGN KEY (trabalhadores_id_trab) REFERENCES trabalhadores(id_trab);
ALTER TABLE enfermeiro ADD CONSTRAINT enfermeiro_fk1 FOREIGN KEY (trabalhadores_id_trab) REFERENCES trabalhadores(id_trab);
ALTER TABLE assistente ADD CONSTRAINT assistente_fk1 FOREIGN KEY (trabalhadores_id_trab) REFERENCES trabalhadores(id_trab);
ALTER TABLE consulta ADD CONSTRAINT consulta_fk1 FOREIGN KEY (fatura_id_fatura) REFERENCES fatura(id_fatura);
ALTER TABLE consulta ADD CONSTRAINT consulta_fk2 FOREIGN KEY (medico_trabalhadores_id_trab) REFERENCES medico(trabalhadores_id_trab);
ALTER TABLE consulta ADD CONSTRAINT consulta_fk3 FOREIGN KEY (pacientes_id_pac) REFERENCES pacientes(id_pac);
ALTER TABLE internamento ADD CONSTRAINT internamento_fk1 FOREIGN KEY (pacientes_id_pac) REFERENCES pacientes(id_pac);
ALTER TABLE internamento ADD CONSTRAINT internamento_fk2 FOREIGN KEY (fatura_id_fatura) REFERENCES fatura(id_fatura);
ALTER TABLE internamento ADD CONSTRAINT internamento_fk3 FOREIGN KEY (enfermeiro_trabalhadores_id_trab) REFERENCES enfermeiro(trabalhadores_id_trab);
ALTER TABLE cirurgia ADD CONSTRAINT cirurgia_fk1 FOREIGN KEY (internamento_id_inter) REFERENCES internamento(id_inter);
ALTER TABLE cirurgia ADD CONSTRAINT cirurgia_fk2 FOREIGN KEY (medico_trabalhadores_id_trab) REFERENCES medico(trabalhadores_id_trab);
ALTER TABLE pagamento ADD CONSTRAINT pagamento_fk1 FOREIGN KEY (fatura_id_fatura) REFERENCES fatura(id_fatura);
ALTER TABLE caract_efeit_sec ADD CONSTRAINT caract_efeit_sec_fk1 FOREIGN KEY (efeito_secundario_id_efeito) REFERENCES efeito_secundario(id_efeito);
ALTER TABLE caract_efeit_sec ADD CONSTRAINT caract_efeit_sec_fk2 FOREIGN KEY (medicamento_id_medicamento) REFERENCES medicamento(id_medicamento);
ALTER TABLE dosagem ADD CONSTRAINT dosagem_fk1 FOREIGN KEY (medicamento_id_medicamento) REFERENCES medicamento(id_medicamento);
ALTER TABLE dosagem ADD CONSTRAINT dosagem_fk2 FOREIGN KEY (receita_id_receita) REFERENCES receita(id_receita);
ALTER TABLE consulta_enfermeiro ADD CONSTRAINT consulta_enfermeiro_fk1 FOREIGN KEY (consulta_id_cons) REFERENCES consulta(id_cons);
ALTER TABLE consulta_enfermeiro ADD CONSTRAINT consulta_enfermeiro_fk2 FOREIGN KEY (enfermeiro_trabalhadores_id_trab) REFERENCES enfermeiro(trabalhadores_id_trab);
ALTER TABLE receita_consulta ADD CONSTRAINT receita_consulta_fk1 FOREIGN KEY (receita_id_receita) REFERENCES receita(id_receita);
ALTER TABLE receita_consulta ADD CONSTRAINT receita_consulta_fk2 FOREIGN KEY (consulta_id_cons) REFERENCES consulta(id_cons);
ALTER TABLE internamento_receita ADD CONSTRAINT internamento_receita_fk1 FOREIGN KEY (internamento_id_inter) REFERENCES internamento(id_inter);
ALTER TABLE internamento_receita ADD CONSTRAINT internamento_receita_fk2 FOREIGN KEY (receita_id_receita) REFERENCES receita(id_receita);
ALTER TABLE cirurgia_enfermeiro ADD CONSTRAINT cirurgia_enfermeiro_fk1 FOREIGN KEY (cirurgia_id_cirur) REFERENCES cirurgia(id_cirur);
ALTER TABLE cirurgia_enfermeiro ADD CONSTRAINT cirurgia_enfermeiro_fk2 FOREIGN KEY (enfermeiro_trabalhadores_id_trab) REFERENCES enfermeiro(trabalhadores_id_trab);
ALTER TABLE especializacao ADD CONSTRAINT especializacao_fk1 FOREIGN KEY (id_medico) REFERENCES medico(trabalhadores_id_trab);
ALTER TABLE especializacao_especializacao ADD CONSTRAINT especializacao_especializacao_fk1 FOREIGN KEY (especializacao_id_espec) REFERENCES especializacao(id_espec);
ALTER TABLE especializacao_especializacao ADD CONSTRAINT especializacao_especializacao_fk2 FOREIGN KEY (especializacao_id_espec1) REFERENCES especializacao(id_espec);




/*ALTER TABLE medico_especializacao ADD CONSTRAINT medico_especializacao_fk1 FOREIGN KEY (medico_trabalhadores_id_trab) REFERENCES medico(trabalhadores_id_trab);
ALTER TABLE medico_especializacao ADD CONSTRAINT medico_especializacao_fk2 FOREIGN KEY (especializacao_id_espec) REFERENCES especializacao(id_espec);
*/

/*
CREATE TABLE medico_especializacao (
	medico_trabalhadores_id_trab INTEGER,
	especializacao_id_espec	 INTEGER,
	PRIMARY KEY(medico_trabalhadores_id_trab,especializacao_id_espec)
);
*/