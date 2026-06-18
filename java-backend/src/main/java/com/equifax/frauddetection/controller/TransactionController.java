package com.equifax.frauddetection.controller;

import com.equifax.frauddetection.model.Transaction;
import com.equifax.frauddetection.service.TransactionService;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/transactions")
public class TransactionController {

    private final TransactionService transactionService;

    public TransactionController(TransactionService transactionService) {
        this.transactionService = transactionService;
    }

    @PostMapping
    public Transaction submitTransaction(@RequestBody Transaction transaction) {
        return transactionService.processTransaction(transaction);
    }
}
