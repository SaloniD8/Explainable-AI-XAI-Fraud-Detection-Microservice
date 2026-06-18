package com.equifax.frauddetection.repository;

import com.equifax.frauddetection.model.Transaction;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TransactionRepository extends JpaRepository<Transaction, Long> {
}
